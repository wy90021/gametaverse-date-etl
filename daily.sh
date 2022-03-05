#if [ -z "$1" ]
#then
#      echo "need starting date input, e.g. bash daily.sh 2021-12-20"
#      exit 0
#fi
#d=$1
d=$(date +%F)

bash block-script.sh $d &&
bash etl-script.sh $d &&
python3 daily-agg/process.py $d &&
bash upload_s3.sh $d gametaverse-starsharks-daily preprocessed
# bash ~/gametaverse-date-etl/dynamo-scripts.sh $d prod
