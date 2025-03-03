GIT_REPO="https://git.nju.edu.cn/api/v4/projects/13817"
GIT_HEAD="PRIVATE-TOKEN: $GITLAB_TOKEN"

BOX_REPO="https://box.nju.edu.cn/api2/repos/cdd3071b-dce0-486d-8e6d-497a921a340d"
BOX_HEAD="Authorization: Token $BOX_TOKEN"
BOX_UPLOAD_URL=$( curl -sSf -H "$BOX_HEAD" "$BOX_REPO/upload-link/" | tr -d "\"" )

curl -sSf -H "$GIT_HEAD" "$GIT_REPO/repository/files/html_targets.txt/raw" \
| python3 main.py \
> png_targets.txt

# upload to box
curl -sSf -F file=@png_targets.txt -F parent_dir=/ -F replace=1 "$BOX_UPLOAD_URL"
rm png_targets.txt

# trigger next steps
curl -sSf -H "$GIT_HEAD" "$GIT_REPO/pipeline?ref=main" -X POST
