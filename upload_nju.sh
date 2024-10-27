REPO="https://log2:$PASSWORD@git.nju.edu.cn/log2/zyf_data.git"

git clone -q $REPO tmp && cd tmp
trap "cd .. && rm -rf tmp" EXIT

git config user.email "log2cn@gmail.com"
git config user.name "log2"

git push -q origin --delete a
git checkout -b a

touch a.txt
git add .
git commit -m "upload from nju" > /dev/null
git push -q origin list 2>&1 | grep -v "^remote:"