echo $(rclone cat box:data.json) | jq -c '.[]' | while read -r img; do
  path=data/$(echo "$img" | jq -r '.[0]')
  url=$(echo "$img" | jq -r '.[1]')

  mkdir -p $(dirname $path)
  curl -s -o $path $url
  
  if [[ $? -ne 0 ]]; then
    curl -o $path $url
  fi
done

time rclone move --delete-empty-src-dirs data/ box:data/
