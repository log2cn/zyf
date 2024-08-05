import requests
import re
import os
import time
import traceback

TIMEOUT = 10

from webdav3.client import Client
options = {
    'webdav_hostname': 'https://box.nju.edu.cn/seafdav/zyf_imgs/',
    'webdav_login': '502023330057@nju.edu.cn',
    'webdav_password': os.environ.get('PASSWORD'),
}
client = Client(options)

def check_parent_dir(remote_path):
    dir = os.path.dirname(remote_path)
    if not client.check(dir):
        check_parent_dir(dir)
    client.mkdir(dir)

upload_tmp_file = "tmp"
def binary_string_to_file(binary_string):
    with open(upload_tmp_file, "wb") as file:
        file.write(binary_string)

def upload(remote_dir,name,binary_string):
    if check_box_has(remote_dir,name,binary_string):
        return
    remote_path = os.path.join(remote_dir, name)
    check_parent_dir(remote_path)
    binary_string_to_file(binary_string)
    local_path = upload_tmp_file
    client.upload_sync(remote_path, local_path)

def try_download_and_upload_img(path, name, url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if len(response.content) > 1000:
            upload(path, name, response.content)
            return "1"
        if "502" in response.text:
            return "0"
        if response.status_code == 404:
            return "4"
        return response.status_code, response.text
    except:
        return "t"
    
array_file_name = "array.txt"
def read_remote_array():
    if client.check(array_file_name):
        client.download_sync(array_file_name, array_file_name)
        with open(array_file_name, 'r') as file:
            return eval(file.read())
imgs = read_remote_array()

def save_remote_array(array):
    with open(array_file_name, 'w') as file:
        file.write(str(array))
    client.upload_sync(array_file_name, array_file_name)

def check_box_has(remote_dir,name,binary_string):
    remote_path = os.path.join(remote_dir, name)
    if client.check(remote_path):
        return True

def try_remove_file(filename):
    if os.path.exists(filename):
        print(f"删除{filename}")
        os.remove(filename)

for i in range(10):
    print("imgs:", len(imgs))
    imgs_ = []
    for img in imgs:
        result = try_download_and_upload_img(*img)
        print(result, end=",", flush=True)
        if not check_box_has(*img) and result != "4":
            imgs_.append(img)
    imgs = imgs_
print("")
try_remove_file("tmp")
try_remove_file("array.txt")