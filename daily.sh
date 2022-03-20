if [ -z "$1" ]
then
    d=$(date --date="yesterday" +"%Y-%m-%d")
else
    d=$1
fi
echo $d
bash block-script.sh $d && 
bash etl-script.sh $d &&
python3 daily-agg/process.py $d &&
bash upload_price_history.sh &&
bash upload_s3.sh $d gametaverse-daily/starsharks preprocessed &&
bash preload_cache.sh $d