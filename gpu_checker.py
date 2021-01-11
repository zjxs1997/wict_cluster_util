# todo: add gpu_blacklist support
# todo: colorful display
# miner change to test github push

import requests
import json
import colorama

target_memory = 1000

cluster_blacklist = [2]
gpu_blacklist = [(7, 'GPU0')]

r = requests.get("http://172.31.32.100/gpustat/info.js")
text = r.text
json_text = text[6:-2]
state_dict = json.loads(json_text)

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
            print(f"{cluster_key} | GPU{gpu_key} | 使用显存 {gpu_value['memory.used']: 5} | 使用率 {gpu_value['utilization.gpu']:3} | 温度 {gpu_value['temperature.gpu']}")
