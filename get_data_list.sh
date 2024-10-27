git clone -q -b list https://$TOKEN@git.nju.edu.cn/log2/zyf_data.git tmp && cd tmp
git push -q origin --delete list
mv -f ./* ..
cd ..
rm -rf tmp
