if [ -z "$1" ]
then
  echo "need starting date input, e.g. bash clear_cache.sh 2021-12-20"
  exit 0
else
  d=$1
fi
today=$(date +"%Y-%m-%d")
echo "today: $today"
while [ "$d" != $today ]; do 
  echo "clearing cache for : $d"
#   aws s3 --recursive rm s3://gametaverse-daily --exclude "*" --include "starsharks/cache/*$d*/*" --profile default
#   bash preload_cache.sh $d
  aws s3 --recursive rm s3://gametaverse-daily-starsharks --exclude "*" --include "cache/*$d*/*" --profile prod
  d=$(date -I -d "$d + 1 day")
done

d=$1
while [ "$d" != $today ]; do 
  bash scripts/preload_cache.sh $d
  d=$(date -I -d "$d + 1 day")
done



