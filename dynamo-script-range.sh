if [ -z "$1" ]
then
      echo "need date input, e.g. bash dynamo-script-range.sh 2021-12-16 prod 13524255 13538941 "
      exit 0
fi
env="local"
if [ -n "$2" ]
then
      echo "set env to $2"
      env=$2
fi

echo "Populating gametaverse-new-user-time, gametaverse-starsharks-transfer, gametaverse-user-profile table"
python3 get_user_transactions.py --env ${env} $1/in-game-token-transfers-$3-$4.csv
