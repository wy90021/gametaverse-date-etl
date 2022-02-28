if [ -z "$1" ]
then
      echo "need starting date input, e.g. bash upload_s3.sh 2021-12-20"
      exit 0
fi
today=$(date +"%Y-%m-%d")
echo "today: $today"
d=$1
while [ "$d" != $today ]; do 
  echo $d
  python3 daily-agg/process.py $d
  d=$(date -I -d "$d + 1 day")
done
