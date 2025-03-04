GIT_REPO="https://git.nju.edu.cn/api/v4/projects/13817"
GIT_HEAD="PRIVATE-TOKEN: $GITLAB_TOKEN"

# html_targets -> png_targets
curl -sSf -H "$GIT_HEAD" "$GIT_REPO/repository/files/html_targets.txt/raw" \
| python3 main.py \
| tr '\n' ' ' \
| curl -sSf -X PUT -H "$GIT_HEAD" "$GIT_REPO/variables/PNG_TARGETS" --form "value=$(cat)" \
| wc -c

# trigger next steps
curl -sSf -X POST -H "$GIT_HEAD" "$GIT_REPO/pipeline?ref=main" 
