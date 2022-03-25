if [ -z "$1" ]
then
      echo "need starting date input, e.g. bash catch-up.sh 2021-12-20"
      exit 0
fi
d=$1
today=$(date +"%Y-%m-%d")
echo "today: $today"
while [ "$d" != $today ]; do 
  echo $d
  bash daily.sh $d
  d=$(date -I -d "$d + 1 day")
done






