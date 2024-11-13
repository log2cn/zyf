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

from sys import stderr
from time import strftime, strptime
import requests
import re
def get_nmc_imgs(target):
    try:
        url_nmc = f"http://www.nmc.cn/publish/{target}"
        text = requests.get(url_nmc).text
        for match in re.finditer(r'data-img="(.*?)"', text):
            url = match.group(1).split('?')[0]
            time = strptime(re.search(r"\d{12}", url).group(), "%Y%m%d%H%M")
            path = strftime(get_path(target), time)
            yield path, url
    except Exception as e:
        print(f"{target}: {e.__class__.__name__}: {e}", file=stderr)

from sys import stdin
def read_targets():
    for line in stdin:
        if line and not line.startswith('#'):
            yield line

for target in read_targets():
    for path, url in get_nmc_imgs(target):
        print(path, url)