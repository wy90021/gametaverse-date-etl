d=$1
while [ "$d" != $2 ]; do 
  bash scripts/preload_cache.sh $d
  d=$(date -I -d "$d + 1 day")
done
