echo $(cat data.json) | jq -c '.[]' | while read -r img; do
  local_path=$(echo "$img" | jq -r '.[0]')
  img_url=$(echo "$img" | jq -r '.[1]')

  mkdir -p data/$(dirname $local_path)

  for ((i=0; i<5; i++)); do
    curl -s -o $local_path $img_url
    if [[ $? -eq 0 ]]; then
      echo "$local_path i"
      break
    fi
  done
done