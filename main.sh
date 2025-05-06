REPO="https://git.nju.edu.cn/api/v4/projects/13817"
CURL="curl -sSf -H PRIVATE-TOKEN:$GITLAB_TOKEN --retry 3"

$CURL $REPO/repository/files/html_targets.txt/raw \
| python3 main.py \
| tee >(wc -l) \
  >(sed -n     1,500p | tr '\n' ' ' | xargs -I {} $CURL $REPO/variables/PNG_TARGETS0 -X PUT -F value={} | wc -c) \
  >(sed -n  501,1000p | tr '\n' ' ' | xargs -I {} $CURL $REPO/variables/PNG_TARGETS1 -X PUT -F value={} | wc -c) \
  >(sed -n 1001,1500p | tr '\n' ' ' | xargs -I {} $CURL $REPO/variables/PNG_TARGETS2 -X PUT -F value={} | wc -c) \
> /dev/null

$CURL $REPO/pipeline?ref=main -X POST | wc -c
