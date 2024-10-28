rclone copy box:/data.json .

echo $(cat data.json) | jq -c '.[]' | while read -r img; do
  path=data/$(echo "$img" | jq -r '.[0]')
  url=$(echo "$img" | jq -r '.[1]')

  mkdir -p $(dirname $path)

  curl -s -o $path $url
  if [[ $? -eq 0 ]]; then
    curl -o $path $url
  fi
done

ls data
rclone move --delete-empty-src-dirs data/ box:data/
