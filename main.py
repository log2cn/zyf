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

def upload(remote_path, binary_string):
    check_parent_dir(remote_path)
    with open(upload_tmp_file, "wb") as file:
        file.write(binary_string)
    client.upload_sync(remote_path, upload_tmp_file)
    os.remove(upload_tmp_file)

def try_download_and_upload_to_box(path, name, url):
    remote_path = os.path.join(path, name)
    if client.check(remote_path):
        return "e" # exists
    try:
        response = requests.get(url)
        if len(response.content) > 1000:
            upload(remote_path, response.content)
            return "u" # upload
        if response.status_code == 404:
            return "4"
        if "502" in response.text:
            return "5"
        return f"{response.status_code}:len={len(response.text)}"
    except Exception as e:
        return type(e).__name__
    
client.download_sync(array_file_name, array_file_name)
with open(array_file_name, 'r') as file:
    imgs = eval(file.read())
os.remove(array_file_name)

for i in range(10):
    print("\nimgs:", len(imgs))
    imgs_ = []
    for img in imgs:
        result = try_download_and_upload_to_box(*img)
        print(result, end=",", flush=True)
        if result not in "eu4":
            imgs_.append(img)
    imgs = imgs_