if [ -z "$1" ]
then
      echo "need starting date input, e.g. bash daily.sh 2021-12-20"
      exit 0
fi
d=$1

bash block-script.sh $d prod
bash etl-script.sh $d
bash dynamo-scripts.sh $d prod
