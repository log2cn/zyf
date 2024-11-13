export PYTHONDONTWRITEBYTECODE=1 # disable __pycache__ 
DATA_DIR=data

curl -sS --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://git.nju.edu.cn/api/v4/projects/log2%2fzyf_nas/repository/files/nmc_targets.txt/raw?ref=main" \
  | python3 main.py \
  | while read -r path url; do
    path="$DATA_DIR/$path"
    mkdir -p $(dirname $path)
    curl -sS --retry 5 -o $path $url
    # break # for test
  done

# data -> box
time rclone move --delete-empty-src-dirs $DATA_DIR/ box:$(date +"%Y%m%d_%H%M")/
rmdir $DATA_DIR

# trigger next steps
curl -sS -o /dev/null -X POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "https://git.nju.edu.cn/api/v4/projects/log2%2fzyf_nas/pipeline?ref=main"
