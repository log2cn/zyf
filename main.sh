REPO="https://git.nju.edu.cn/api/v4/projects/13817"
CURL="curl -sSf -H PRIVATE-TOKEN:$GITLAB_TOKEN --retry 3"

set -x
$CURL "$REPO/repository/files/html_targets.txt/raw" \
| python3 main.py \
| tr '\n' ' ' \
> png_targets.txt

$CURL "$REPO/variables/PNG_TARGETS" -X PUT -F "value=@png_targets.txt" | wc -c

$CURL "$REPO/pipeline?ref=main" -X POST
