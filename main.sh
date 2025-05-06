REPO="https://git.nju.edu.cn/api/v4/projects/13817"
CURL="curl -sSf -H PRIVATE-TOKEN:$GITLAB_TOKEN --retry 3"

$CURL $REPO/repository/files/html_targets.txt/raw | python3 main.py > png_targets.txt

$CURL $REPO/variables/PNG_TARGETS0 -X DELETE
$CURL $REPO/variables/PNG_TARGETS1 -X DELETE
$CURL $REPO/variables/PNG_TARGETS2 -X DELETE

sed -n     1,500p png_targets.txt | tr '\n' ' ' | xargs -I {} $CURL $REPO/variables/PNG_TARGETS0 -X POST -F value={} | wc -c
sed -n  501,1000p png_targets.txt | tr '\n' ' ' | xargs -I {} $CURL $REPO/variables/PNG_TARGETS1 -X POST -F value={} | wc -c
sed -n 1001,1500p png_targets.txt | tr '\n' ' ' | xargs -I {} $CURL $REPO/variables/PNG_TARGETS2 -X POST -F value={} | wc -c

$CURL $REPO/pipeline?ref=main -X POST | wc -c
