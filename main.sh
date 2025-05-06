REPO="https://git.nju.edu.cn/api/v4/projects/13817"
CURL="curl -sSf -H PRIVATE-TOKEN:$GITLAB_TOKEN --retry 3"

$CURL "$REPO/repository/files/html_targets.txt/raw" \
| python3 main.py \
| tee >(wc -l) \
  >(sed -n   '1,200p' | tr '\n' ' ' | $CURL "$REPO/variables/PNG_TARGETS0" -X PUT -F value=@- | wc -c) \
  >(sed -n '201,400p' | tr '\n' ' ' | $CURL "$REPO/variables/PNG_TARGETS1" -X PUT -F value=@- | wc -c) \
  >(sed -n '401,600p' | tr '\n' ' ' | $CURL "$REPO/variables/PNG_TARGETS1" -X PUT -F value=@- | wc -c) \
> /dev/null

$CURL "$REPO/pipeline?ref=main" -X POST | wc -c
