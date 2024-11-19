def get_path(target):
    # split ext
    assert target.count('.') == 1, "target.count('.') != 1"
    target_ext = target.split(".")[1] # htm or html
    target = target.split(".")[0]

    # default
    dirname = target.replace("/","-")
    path = "%Y%m/%Y%m%d/%Y%m%d_%H%Mz.png"
    no_match = False
    
    if target.startswith("observations/"):
        if target.endswith("heavyrain") or target.endswith("gale"):
            path = "%Y%m/%Y%m%d/%Y%m%d_%H%M.png" # no "z"
        elif target.endswith("24hour-precipitation"):
            path = "%Y%m/24hour_%Y%m%d_%H%Mz.png"
        elif "/dm/" in target:
            prefix = target.split("/")[1] + "_" + target[-4:]
            path = f"%Y%m/{prefix}_%Y%m%d_%H%Mz.png"
        elif target.startswith("observations/hourly-"):
            pass
        else:
            no_match = True
    elif target.startswith("radar/"):
        prefix = target.split("/")[-1]
        path = f"%Y%m/%Y%m%d/{prefix}_%Y%m%d_%H%Mz.png"
        if target_ext == "htm":
            dirname = target.replace("/", "-", 1)
        elif target_ext == "html":
            pass
        else:
            no_match = True
    elif target.startswith("tianqishikuang/"):
        dirname = dirname.replace("-index", "")
    elif target.startswith("satellite/"):
        pass
    else:
        no_match = True

    if no_match:
        raise Exception(f"no match: {target}")

    return dirname + "/" + path

from datetime import datetime
def extract_time(url):
    time_str = re.search(r"\d{12}", url).group()
    time = datetime.strptime(time_str, "%Y%m%d%H%M")
    return time

import requests
def get_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

import re
IMG_PATTERN = re.compile(r'data-img="(.*?)"')

def get_image_urls(target):
    url = f"http://www.nmc.cn/publish/{target}"
    for match in IMG_PATTERN.finditer(get_text(url)):
        image_url = match.group(1).split('?')[0]
        save_path = extract_time(url).strftime(get_path(target))
        yield image_url, save_path

from sys import stdin, stderr
for line in stdin:
    target = line.split("#")[0].strip()
    if target:
        try:
            for image_url, save_path in get_image_urls(target):
                print(image_url, save_path)
        except Exception as e:
            print(f"{target}: {e.__class__.__name__}: {e}", file=stderr)
