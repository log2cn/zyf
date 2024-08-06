import requests, os, time

array_file_name = "array.txt"
upload_tmp_file_name = "tmp"

from webdav3.client import Client
options = {
    'webdav_hostname': 'https://box.nju.edu.cn/seafdav/zyf_imgs/',
    'webdav_login': '502023330057@nju.edu.cn',
    'webdav_password': os.environ.get('PASSWORD'),
}
client = Client(options)

def check_parent_dir_recursive(remote_path):
    dir = os.path.dirname(remote_path)
    if not client.check(dir):
        check_parent_dir_recursive(dir)
    client.mkdir(dir)

def upload(remote_path, binary_string):
    check_parent_dir_recursive(remote_path)
    with open(upload_tmp_file_name, "wb") as file:
        file.write(binary_string)
    client.upload_sync(remote_path, upload_tmp_file_name)
    os.remove(upload_tmp_file_name)

def try_download_img(path, name, url):
    remote_path = os.path.join(path, name)
    if client.check(remote_path):
        return "e" # exists
    try:
        response = requests.get(url)
        if len(response.content) > 1000:
            upload(remote_path, response.content)
            return "u"
        if response.status_code == 404:
            return "4"
        if response.status_code == 502:
            return "5"
        return response.status_code
    except Exception as e:
        return type(e).__name__

def try_download_array():
    for i in range(100):
        try:
            client.download_sync(array_file_name, array_file_name)
            with open(array_file_name, 'r') as file:
                imgs = eval(file.read())
            os.remove(array_file_name)
            return imgs
        except Exception as e:
            print("try_download_array:", type(e).__name__) 
            time.sleep(6)
    raise Exception("try_download_array")

imgs = try_download_array()
for i in range(10):
    print("\nimgs:", len(imgs))
    imgs_ = []
    for img in imgs:
        result = try_download_img(*img)
        print(result, end=",", flush=True)
        if result not in "eu4":
            imgs_.append(img)
    imgs = imgs_