mkdir tmp && cd tmp
trap "cd .. && rm -rf tmp" EXIT

mv ../upload/* .

git init --initial-branch=main 
REPO_URL="https://log2:$PASSWORD@git.nju.edu.cn/log2/zyf_data.git"
git remote add origin "$REPO_URL"
git add .
git config user.email "log2cn@gmail.com"
git config user.name "log2"

git checkout -b $(xxd -p -l 8 /dev/urandom)

git commit -m "upload files"
git push -u -q origin "$branch_name" 2>&1 | grep -v '^remote:'
