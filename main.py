import re
from sys import stdin, stderr

def get_path_fmt(target):
    # split ext
    assert target.count('.') == 1, "target.count('.') != 1"
    target_ext = target.split(".")[1] # htm or html
    target = target.split(".")[0]

    # default
    dirname = target.replace("/","-")
    path = "%Y%m/%Y%m%d/%Y%m%d_%H%Mz.png"
    
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
            print(f"no match for observations/: {target}", file=stderr)
    elif target.startswith("radar/"):
        prefix = target.split("/")[-1]
        path = f"%Y%m/%Y%m%d/{prefix}_%Y%m%d_%H%Mz.png"
        if target_ext == "htm":
            dirname = target.replace("/", "-", 1)
        elif target_ext == "html":
            pass
        else:
            print(f"no match for radar/: {target}", file=stderr)
    elif target.startswith("tianqishikuang/"):
        dirname = dirname.replace("-index", "")
    elif target.startswith("satellite/"):
        pass
    else:
        print(f"no match: {target}", file=stderr)

    return dirname + "/" + path

TIME_REGEX = re.compile(r"\d{12}")
from datetime import datetime
def extract_time(url):
    time_str = TIME_REGEX.search(url).group()
    return datetime.strptime(time_str, "%Y%m%d%H%M")

import requests
def get_text(url):
    with requests.get(url) as response:
        response.raise_for_status()
        return response.text

IMG_PATTERN = re.compile(r'data-img="(.*?)"')
def get_image_urls(target):
    url = f"http://www.nmc.cn/publish/{target}"
    path_fmt = get_path_fmt(target)
    for match in IMG_PATTERN.finditer(get_text(url)):
        url  = match.group(1).split('?')[0]
        path = extract_time(url).strftime(path_fmt)
        yield url, path

for target in stdin:
    target = target.strip()
    if not target or target.startswith('#'):
        continue
    try:
        for array in get_image_urls(target):
            print(*array)
    except Exception as e:
        print(f"{target}: {e.__class__.__name__}: {e}", file=stderr)
