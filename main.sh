export PYTHONDONTWRITEBYTECODE=1 # disable __pycache__ 
export TARGETS=nmc_targets.py
export DATA_DIR=data

# download TARGETS for python
curl -sS -o $TARGETS --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "https://git.nju.edu.cn/api/v4/projects/log2%2fzyf_nas/repository/files/nmc_targets.py/raw?ref=main"

# download data
python3 main.py -i $TARGETS | while read -r path url; do
  path=$DATA_DIR/$path
  mkdir -p $(dirname $path)
  curl -sS --retry 5 -o $path $url

  if [ ! -f /.dockerenv ]; then
    break # for test
  fi
done
rm $TARGETS

# data -> box
time rclone move --delete-empty-src-dirs $DATA_DIR/ box:$(date +"%Y%m%d_%H%M")/
rmdir $DATA_DIR

# trigger next steps
curl -sS -o /dev/null -X POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "https://git.nju.edu.cn/api/v4/projects/log2%2fzyf_nas/pipeline?ref=main"