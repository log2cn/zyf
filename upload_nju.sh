git clone -q https://log2:$PASSWORD@git.nju.edu.cn/log2/zyf_data.git tmp && cd tmp
trap "cd .. && rm -rf tmp" EXIT

git config user.email "log2cn@gmail.com"
git config user.name "log2"

echo $(xxd -p -l 8 /dev/urandom) > rand.txt
git add .
git commit -m "upload from nju" > /dev/null
git push -q origin main 2>&1 | grep -v "^remote:"