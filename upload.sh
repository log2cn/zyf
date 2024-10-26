mkdir tmp && cd tmp
trap "cd .. && rm -rf tmp" EXIT

mv ../upload/* .

git init --initial-branch=main 
git remote add origin "https://log2:$PASSWORD@git.nju.edu.cn/log2/zyf_data.git"

git config user.email "log2cn@gmail.com"
git config user.name "log2"

branch_name=$(xxd -p -l 8 /dev/urandom)
git checkout -b $branch_name
git add .
git commit -m "upload files from github" > /dev/null
git push -u origin $branch_name
