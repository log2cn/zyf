echo $(rclone cat box:data.json) | jq -c '.[]' | while read -r img; do
  path=data/$(echo "$img" | jq -r '.[0]')
  url=$(echo "$img" | jq -r '.[1]')

  mkdir -p $(dirname $path)
  curl -sS --retry 5 -o $path $url
done

time rclone move --delete-empty-src-dirs data/ box:data/
