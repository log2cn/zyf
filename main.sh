REPO="https://git.nju.edu.cn/api/v4/projects/13817"
CURL="curl -sSf -H PRIVATE-TOKEN:$GITLAB_TOKEN --retry 3"

echo "$(date "+%H:%M:%S"): get html_targets.txt, run main.py, save to png_targets.txt"
$CURL $REPO/repository/files/html_targets.txt/raw | python3 main.py > png_targets.txt
wc -l png_targets.txt

echo "$(date "+%H:%M:%S"): delete variables"
$CURL $REPO/variables/PNG_TARGETS0 -X DELETE
$CURL $REPO/variables/PNG_TARGETS1 -X DELETE
$CURL $REPO/variables/PNG_TARGETS2 -X DELETE

echo "$(date "+%H:%M:%S"): create variables"
sed -n     1,500p png_targets.txt | tr '\n' ' ' | $CURL $REPO/variables -X POST -F key=PNG_TARGETS0 -F "value=$(cat)" | wc -c
sed -n  501,1000p png_targets.txt | tr '\n' ' ' | $CURL $REPO/variables -X POST -F key=PNG_TARGETS1 -F "value=$(cat)" | wc -c
sed -n 1001,1500p png_targets.txt | tr '\n' ' ' | $CURL $REPO/variables -X POST -F key=PNG_TARGETS2 -F "value=$(cat)" | wc -c

echo "$(date "+%H:%M:%S"): create pipeline"
$CURL $REPO/pipeline?ref=main -X POST | wc -c
