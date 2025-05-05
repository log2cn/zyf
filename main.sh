REPO="https://git.nju.edu.cn/api/v4/projects/13817"
CURL="curl -sSf -H PRIVATE-TOKEN:$GITLAB_TOKEN --retry 3"

# html_targets -> png_targets
$CURL "$REPO/repository/files/html_targets.txt/raw" \
| tee >(head -n 10) >(wc -l) \
| python3 main.py \
| tr '\n' ' ' \
| xargs -I {} $CURL "$REPO/variables/PNG_TARGETS" -X PUT -F "value={}" \
| wc -c

# trigger next steps
$CURL "$REPO/pipeline?ref=main" -X POST
