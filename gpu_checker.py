# todo: colorful display
# todo: add wechat notification
# todo: use a configuration file
#       or use input from cmd line to overwrite

import requests
import json
import colorama
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--target_memory', type=int, default=1000)
parser.add_argument('--group_name', type=str, default='LCWM')

parser.add_argument('--wechat_notify', action='store_true')
parser.add_argument('--wechat_sckey', type=str,)
parser.add_argument('--wechat_notify_interval', type=int, default=24*3600)
parser.add_argument('--black_list', type=str, nargs='+')


args = parser.parse_args()


target_memory = 1000

cluster_blacklist = [2]
your_group_codename = 'LCWM'
gpu_blacklist = []
if args.black_list:
    for black in args.black_list:
        num = int(black[0])
        gpu_num = 'GPU' + black[1]
        gpu_blacklist.append((num, gpu_num))
# [(7, 'GPU0')]


use_wechat_notify = False
wechat_schkey = 'xxx'
notify_every_seconds = 3600*24
# 可以把上次通知时间写到本地某个文件里，每次读取，比较是否经过那么多时间

r = requests.get("http://172.31.32.100/gpustat/info.js")
text = r.text
json_text = text[6:-2]
state_dict = json.loads(json_text)

texts = []

for i in range(10):
    if i in cluster_blacklist:
        continue
    cluster_key = 'icst' + str(i)
    for gpu_key, gpu_value in state_dict[cluster_key].items():
        black_flag = False
        for black_i, black_gpu in gpu_blacklist:
            if i == black_i and gpu_key == black_gpu:
                black_flag = True
                break
        if black_flag:
            continue

        if gpu_value['memory.used'] <= target_memory:
            text = f"{cluster_key} | GPU{gpu_key} | 使用显存 {gpu_value['memory.used']: 5} | 使用率 {gpu_value['utilization.gpu']:3} | 温度 {gpu_value['temperature.gpu']}"
            print(text)
            texts.append(text)

print()
group_gpu_thread_dict = state_dict['top_group_gpu_threads']
if your_group_codename in group_gpu_thread_dict:
    number = group_gpu_thread_dict[your_group_codename]
    print(f'{your_group_codename}: {number}')

