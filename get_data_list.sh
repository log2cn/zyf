REPO_URL="https://$TOKEN@github.com/l0g2/zyf_imgs.git"

if ! git ls-remote --heads "$REPO_URL" list | grep -q list ; then
    exit
fi

git clone -q -b list https://$TOKEN@github.com/l0g2/zyf_imgs.git tmp && cd tmp
git push -q origin --delete list
mv ./* ..
cd ..
rm -rf tmp
ls
