if [ -z "$1" ]
then
    d=$(date --date="yesterday" +"%Y-%m-%d")
else
    d=$1
fi
today=$(date +"%Y-%m-%d")
echo "today: $today"
while [ "$d" != $today ]; do 
  echo $d
#   aws s3 --recursive rm s3://gametaverse-daily --exclude "*" --include "starsharks/cache/*$d*/*" --profile default
#   bash preload_cache.sh $d
  aws s3 --recursive rm s3://gametaverse-daily-starsharks --exclude "*" --include "cache/*$d*/*" --profile prod
  bash scripts/preload_cache.sh $d
  d=$(date -I -d "$d + 1 day")
done



