echo $(cat data.json) | jq -c '.[]' | while read -r img; do
  path=data/$(echo "$img" | jq -r '.[0]')
  url=$(echo "$img" | jq -r '.[1]')

  mkdir -p $(dirname $path)

  for ((i=0; i<5; i++)); do
    curl -s -o $path $url
    if [[ $? -eq 0 ]]; then
      echo "$path i"
      break
    fi
  done
done