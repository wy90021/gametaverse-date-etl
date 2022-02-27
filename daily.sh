if [ -z "$1" ]
then
      echo "need starting date input, e.g. bash daily.sh 2021-12-20"
      exit 0
fi
d=$1

bash ~/gametaverse-date-etl/block-script.sh $d prod
bash ~/gametaverse-date-etl/etl-script.sh $d
# bash ~/gametaverse-date-etl/dynamo-scripts.sh $d prod
