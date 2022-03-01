if [ -z "$1" ]
then
      echo "need date input, e.g. bash dynamo-scripts.sh 2022-01-01 prod"
      exit 0
fi
env="local"
if [ -n "$2" ]
then
      echo "set env to $2"
      env=$2
fi

echo "Populating gametaverse-starsharks-transfer"
python3 upload_transfers.py --env ${env} $1/in-game-token-transfers.csv $1/blocks.csv
echo "Populating gametaverse-new-user-time, gametaverse-user-transfer, gametaverse-user-profile table"
python3 upload_user_transactions.py --env ${env} $1/in-game-token-transfers.csv $1/blocks.csv
