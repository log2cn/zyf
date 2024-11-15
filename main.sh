PYTHONDONTWRITEBYTECODE=1 # disable __pycache__ 
GITLAB_REPO="https://git.nju.edu.cn/api/v4/projects/log2%2fzyf_nas"
GITLAB_HEADER="PRIVATE-TOKEN: $GITLAB_TOKEN"

curl -sSf -H "$GITLAB_HEADER" "$GITLAB_REPO/repository/files/nmc_targets.txt/raw" \
| python3 main.py \
> targets.txt

rclone move targets.txt zyf:/

# trigger next steps
curl -sSf -o /dev/null -X POST -H "$GITLAB_HEADER" "$GITLAB_REPO/pipeline?ref=main"
