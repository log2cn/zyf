rclone cat box:data.txt | while read -r path url; do
  mkdir -p $(dirname $path)
  curl -sS --retry 5 -o $path $url
done

time rclone move --delete-empty-src-dirs data/ box:data/
