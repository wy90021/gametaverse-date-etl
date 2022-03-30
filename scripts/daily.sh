if [ -z "$1" ]
then
    d=$(date --date="yesterday" +"%Y-%m-%d")
else
    d=$1
fi
echo $d
bash scripts/block-script.sh $d && 
bash scripts/etl-script.sh $d &&
python3 daily-agg/process.py $d &&
bash scripts/upload_price_history.sh &&
bash scripts/upload_s3.sh $d gametaverse-daily-starsharks preprocessed &&
bash scripts/clear_cache.sh $d
bash scripts/preload_cache.sh $d