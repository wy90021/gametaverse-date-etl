if [ -z "$1" ]
then
      echo "need starting date input, e.g. bash daily.sh 2021-12-20"
      exit 0
fi
d=$1

bash block-script.sh $d
bash etl-script.sh $d
python3 daily-agg/process.py $d
bash upload_price_history.sh
bash upload_s3.sh $d gametaverse-daily/starsharks preprocessed
