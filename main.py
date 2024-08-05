import requests
import os

array_file_name = "array.txt"
upload_tmp_file = "tmp"

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

def binary_string_to_file(binary_string):
    with open(upload_tmp_file, "wb") as file:
        file.write(binary_string)

def upload(remote_dir,name,binary_string):
    remote_path = os.path.join(remote_dir, name)
    check_parent_dir(remote_path)
    binary_string_to_file(binary_string)
    client.upload_sync(remote_path, upload_tmp_file)

def try_download_and_upload_to_box(path, name, url):
    if check_box_has(path, name, url):
        return "e" # exists
    try:
        response = requests.get(url)
        if len(response.content) > 1000:
            upload(path, name, response.content)
            return "u" # upload
        if response.status_code == 404:
            return "4"
        if "502" in response.text:
            return "5"
        return f"{response.status_code}:len={len(response.text)}"
    except Exception as e:
        return type(e).__name__
    
def read_remote_array():
    if client.check(array_file_name):
        client.download_sync(array_file_name, array_file_name)
        with open(array_file_name, 'r') as file:
            return eval(file.read())

def check_box_has(remote_dir,name,binary_string):
    remote_path = os.path.join(remote_dir, name)
    if client.check(remote_path):
        return True

def try_remove_file(filename):
    if os.path.exists(filename):
        print(f"删除{filename}")
        os.remove(filename)

imgs = read_remote_array()
for i in range(10):
    print("imgs:", len(imgs))
    imgs_ = []
    for img in imgs:
        result = try_download_and_upload_to_box(*img)
        print(result, end=",", flush=True)
        if result not in "eu4":
            imgs_.append(img)
    imgs = imgs_
print("")
try_remove_file("tmp")
try_remove_file("array.txt")