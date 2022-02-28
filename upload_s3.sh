if [ -z "$1" ]
then
      echo "need starting date input, e.g. bash upload_s3.sh 2021-12-20 gametaverse-starsharks"
      exit 0
fi

if [ -z "$2" ]
then
      echo "need bucket input, e.g. bash upload_s3.sh 2021-12-20 gametaverse-starsharks"
      exit 0
fi
today=$(date +"%Y-%m-%d")
echo "today: $today"
d=$1
bucket=$2
while [ "$d" != $today ]; do 
  echo $d
  aws s3 cp $d s3://$bucket/$d --recursive --profile s3
  d=$(date -I -d "$d + 1 day")
done
