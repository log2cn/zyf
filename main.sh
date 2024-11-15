REPO="https://git.nju.edu.cn/api/v4/projects/13817"

curl -sSf -H "PRIVATE-TOKEN: $GITLAB_TOKEN" "$REPO/repository/files/nmc_targets.txt/raw" \
| python3 main.py \
> targets.txt

curl -sSf -F file=@targets.txt -F parent_dir=/ -F replace=1 $(
  curl -sSf -H "Authorization: Token $BOX_TOKEN" \
  https://box.nju.edu.cn/api2/repos/cdd3071b-dce0-486d-8e6d-497a921a340d/upload-link/ \
  | tr -d "\""
)

rm targets.txt

# trigger next steps
curl -sSf -H "PRIVATE-TOKEN: $GITLAB_TOKEN" "$REPO/pipeline?ref=main" -X POST > /dev/null
