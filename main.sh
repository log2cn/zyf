REPO="https://git.nju.edu.cn/api/v4/projects/13817"
UPLOAD_URL=$(
  curl -sSf -H "Authorization: Token $BOX_TOKEN" \
  https://box.nju.edu.cn/api2/repos/cdd3071b-dce0-486d-8e6d-497a921a340d/upload-link/ \
  | tr -d "\""
)

curl -sSf -H "PRIVATE-TOKEN: $GITLAB_TOKEN" "$REPO/repository/files/nmc_targets.txt/raw" \
| python3 main.py \
> targets.txt

curl -sSf $UPLOAD_URL \
    -F file=@targets.txt -F parent_dir=/ -F replace=1

rm targets.txt

# trigger next steps
curl -sSf -H "PRIVATE-TOKEN: $GITLAB_TOKEN" "$REPO/pipeline?ref=main" -X POST > /dev/null
