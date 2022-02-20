# No block-timestamps
if [ -z "$1" ]
then
      echo "need starting date input, e.g. bash catch-up.sh 2021-12-20"
      exit 0
fi
d=$1
while [ "$d" != 2022-02-14 ]; do 
  echo $d
  bash etl-script.sh $d
  bash dynamo-scripts.sh $d prod
  d=$(date -I -d "$d + 1 day")
done






