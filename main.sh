export PYTHONDONTWRITEBYTECODE=1 # disable __pycache__ 
DATA_DIR=data
GITLAB_REPO="https://git.nju.edu.cn/api/v4/projects/log2%2fzyf_nas"
GITLAB_HEADER="PRIVATE-TOKEN: $GITLAB_TOKEN"

curl -sSf -H "$GITLAB_HEADER" "$GITLAB_REPO/repository/files/nmc_targets.txt/raw" \
  | python3 main.py \
  | while read -r url path; do
    path="$DATA_DIR/$path"
    mkdir -p $(dirname $path)
    curl -sS --retry 5 -o $path $url
    # break # for test
  done
# exit # for test

# data -> box
time rclone move --delete-empty-src-dirs $DATA_DIR/ box:$(date +"%Y%m%d_%H%M")/
rmdir $DATA_DIR

# trigger next steps
curl -sSf -o /dev/null -X POST -H "$GITLAB_HEADER" "$GITLAB_REPO/pipeline?ref=main"
