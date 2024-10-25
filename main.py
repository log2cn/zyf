import os

from webdav3.client import Client
options = {
    'webdav_hostname': 'https://box.nju.edu.cn/seafdav/zyf_imgs/',
    'webdav_login': '502023330057@nju.edu.cn',
    'webdav_password': os.environ.get('PASSWORD'),
}
box = Client(options)

def eval_remote_file(client, file_name):
    tmp_file_name = "eval_remote_file.tmp"
    client.download_sync(file_name, tmp_file_name)
    with open(tmp_file_name) as temp_file:
        r = eval(temp_file.read())
    os.remove(tmp_file_name)
    return r

def ensure_parent_dir_recursive(client, remote_path):
    dirname = os.path.dirname(remote_path)
    if not client.check(dirname):
        ensure_parent_dir_recursive(client, dirname)
    client.mkdir(dirname)

def upload_binary_string(client, remote_path, binary_string):
    temp_file_name = "upload_binary_string.tmp"
    ensure_parent_dir_recursive(client, remote_path)
    with open(temp_file_name, "wb") as temp_file:
        temp_file.write(binary_string)
    client.upload_sync(remote_path, temp_file_name)
    os.remove(temp_file_name)

def print_no_newline(*args):
    print(*args, flush=True, end=" ")

import requests
def try_process_img(client, func_log, img):
    path, name, url = img
    remote_path = os.path.join(path, name)
    try:
        # if client.check(remote_path): # img exists at client
        #     func_log("e")
        #     return False
        response = requests.get(url)
        if response.status_code == 200:
            upload_binary_string(client, remote_path, response.content)
            save_file(path, name, response.content)
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

def save_file(path, name, binary_string):
    path = os.path.join("upload", path)
    os.makedirs(path, exist_ok=True)
    path = os.path.join(path, name)
    with open(path, 'wb') as f:
        f.write(binary_string)

imgs = eval_remote_file(box, "array.txt") # [[path, name, url], ...]
imgs = imgs[:2]

for i in range(50):
    print("imgs:", len(imgs))
    imgs_need_retry = [] # retry queue
    for img in imgs:
        if try_process_img(box, print_no_newline, img): # need_retry
            imgs_need_retry.append(img)
    if not imgs_need_retry:
        break
    imgs = imgs_need_retry
    print() # newline
