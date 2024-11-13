# curl -sS -o nmc_targets.py --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
#     "https://git.nju.edu.cn/api/v4/projects/log2%2fzyf_nas/repository/files/nmc_targets.py/raw?ref=main"

rclone cat box:data.txt | while read -r path url; do
  path=data/$path
  mkdir -p $(dirname $path)
  curl -sS --retry 5 -o $path $url
done

time rclone move --delete-empty-src-dirs data/ box:$(date +"%Y%m%d_%H%M")/

curl -X POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "https://git.nju.edu.cn/api/v4/projects/log2%2fzyf_nas/pipeline?ref=main"
