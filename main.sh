REPO="https://git.nju.edu.cn/api/v4/projects/13817"
CURL="curl -sSf -H PRIVATE-TOKEN:$GITLAB_TOKEN --retry 3"

set -x
$CURL "$REPO/repository/files/html_targets.txt/raw" \
| python3 main.py \
| tr '\n' ' ' \
| $CURL "$REPO/variables/PNG_TARGETS" -X PUT -F "value=@-" \
| wc -c

# $CURL "$REPO/repository/files/html_targets.txt/raw" \
# | python3 main.py \
# | tr '\n' ' ' \
# | xargs -I {} $CURL "$REPO/variables/PNG_TARGETS" -X PUT -F "value={}" \
# | wc -c

$CURL "$REPO/pipeline?ref=main" -X POST
