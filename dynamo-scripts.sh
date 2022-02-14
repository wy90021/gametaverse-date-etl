if [ -z "$1" ]
then
      echo "need date input, e.g. bash scripts.sh 2022-01-01 prod"
      exit 0
fi
env="local"
if [ -n "$2" ]
then
      echo "set env to $2"
      env=$2
fi

echo "Populating gametaverse-block-timestamp table"
python3 populate_blocks.py --env ${env} $1/blocks.csv

# filter transaction by game contracts, output in-game-transaction-hashes.csv
echo "Get Transaction IDs"
python3 get_game_transactions.py $1 $1/transactions.csv

echo "Populating gametaverse-new-user-time, gametaverse-starsharks-transfer, gametaverse-user-profile table"
python3 get_user_transactions.py --env ${env} $1/in-game-token-transfers.csv
