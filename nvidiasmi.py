import json
import argparse

import colorama
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()


r = requests.get("http://172.31.32.100/gpustat/info.js")
text = r.text
json_text = text[6:-2]
state_dict = json.loads(json_text)

group_name = 'LCWM'
group_gpu_thread_dict = state_dict['top_group_gpu_threads']
number = group_gpu_thread_dict[group_name]
print(f'{group_name}: {number}\n')

green_pattern = ''+ colorama.Fore.GREEN + ' %s ' + colorama.Style.RESET_ALL
red_pattern = ''+ colorama.Fore.RED + ' %s ' + colorama.Style.RESET_ALL
yellow_pattern = ''+ colorama.Fore.YELLOW + ' %s ' + colorama.Style.RESET_ALL

def print_machine(name, state_dict):
    machine_state_dict = state_dict[name]
    gpu_keys = machine_state_dict.keys()
    gpu_keys = sorted(gpu_keys)
    output_string = f'{"mem.used":12}{"mem.total":12}{"util":10}{"temp":10}'
    if name[-1] == '0' or name[-1] == '5' or args.verbose:
        print(output_string)
    print('-' * 50 + '  ' + name)

    for gpu_key in gpu_keys:
        gpu_value = machine_state_dict[gpu_key]

        memory_used = gpu_value['memory.used']
        memory_total = gpu_value['memory.total']
        temprature = gpu_value['temperature.gpu']
        utilization = gpu_value['utilization.gpu']

        output_string = f'{memory_used:10}{memory_total:10}{temprature:8}{utilization:8}'
        if memory_used <= 100:
            pattern = green_pattern
        elif memory_used >= 8000:
            pattern = red_pattern
        else:
            pattern = yellow_pattern
        print(pattern % (output_string))
    if args.verbose:
        print()

for i in range(10):
    key = 'icst' + str(i)
    print_machine(key, state_dict)





