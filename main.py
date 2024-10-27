import os

def save_binary(path, binary_string):
    path = f"data/{path}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as file:
        file.write(binary_string)

def print_no_newline(*args):
    print(*args, flush=True, end=" ")

import requests
def try_download_img(func_log, img):
    path, name, url = img
    path = path + name
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_binary(path, response.content)
            func_log(".")
            return False
        if response.status_code == 404: # out of date
            func_log("4")
            return False
        if response.status_code == 502:
            func_log("5")
            return True
    except Exception as e: # box error, network error
        func_log(type(e).__name__)
        return True

import json
with open('data.json', 'r') as file:
    imgs = json.load(file)

for i in range(50):
    print("imgs:", len(imgs))
    imgs_need_retry = [] # retry queue
    for img in imgs:
        if try_download_img(print_no_newline, img): # need_retry
            imgs_need_retry.append(img)
    if not imgs_need_retry:
        break
    imgs = imgs_need_retry
    print()
