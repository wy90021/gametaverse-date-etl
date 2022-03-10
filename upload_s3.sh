if [ -z "$1" ]
then
      echo "need starting date input, e.g. bash upload_s3.sh 2021-12-20 gametaverse-starsharks-daily preprocessed"
      exit 0
fi

if [ -z "$2" ]
then
      echo "need bucket input, e.g. bash upload_s3.sh 2021-12-20 gametaverse-starsharks-daily preprocessed"
      exit 0
fi

if [ -z "$3" ]
then
      echo "need local folder input, e.g. bash upload_s3.sh 2021-12-20 gametaverse-starsharks-daily preprocessed"
      exit 0
fi
today=$(date +"%Y-%m-%d")
echo "today: $today"
d=$1
bucket=$2
local_folder=$3
aws s3 cp $local_folder/$d s3://$bucket/$d --recursive --profile bo-s3
