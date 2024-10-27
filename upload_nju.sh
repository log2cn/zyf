REPO="https://log2:$PASSWORD@git.nju.edu.cn/log2/zyf_data.git"

git clone -q $REPO tmp && cd tmp
trap "cd .. && rm -rf tmp" EXIT

git config user.email "log2cn@gmail.com"
git config user.name "log2"

branch_name=$(xxd -p -l 8 /dev/urandom)
git checkout -b $branch_name
mkdir data && mv ../data/* ./data && rmdir ../data
git add .
git commit -m "upload from github" > /dev/null
git push -u origin $branch_name 2>&1 | grep -v "^remote:"
