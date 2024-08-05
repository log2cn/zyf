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

def check_and_save_imgs():
    imgs_ = []
    for img in imgs:
        if not check_before_upload(*img):
            imgs_.append(img)
    save_remote_array(imgs_)
    print("\n remote array 更新:", len(imgs_))
    return imgs_

def check_before_upload(remote_dir,name,binary_string):
    remote_path = os.path.join(remote_dir, name)
    if client.check(remote_path):
        return True

print(len(imgs))
for img in imgs:
    result = try_download_and_upload_img(*img)
    print(result, end=",", flush=True)

check_and_save_imgs()