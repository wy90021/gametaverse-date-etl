d=$(date --date="yesterday" +"%Y-%m-%d")

bash block-script.sh $d  &&
bash etl-script.sh $d &&
python3 daily-agg/process.py $d &&
bash upload_price_history.sh &&
bash upload_s3.sh $d gametaverse-daily/starsharks preprocessed
