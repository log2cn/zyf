rclone cat box:data.txt | while read -r path url; do
  path=data/$path
  mkdir -p $(dirname $path)
  curl -sS --retry 5 -o $path $url
done

time rclone move --delete-empty-src-dirs data/ box:data/
