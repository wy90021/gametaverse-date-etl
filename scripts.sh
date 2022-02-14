if [ -z "$1" ]
then
      echo "need date input, e.g. bash scripts.sh 2022-01-01"
      exit 0
fi
env="local"
if [ -n "$2" ]
then
      echo "set env to $2"
      env=$2
fi

range=$(ethereumetl get_block_range_for_date -d $1 --provider-uri https://bsc-dataseed.binance.org/)
rangeArr=(${range//,/ })
echo "Block range for $1: $range"
echo "Env: ${env}"
ethereumetl export_blocks_and_transactions --start-block ${rangeArr[0]} --end-block ${rangeArr[1]} --blocks-output blocks.csv --transactions-output transactions.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100 
python3 populate_blocks.py  --env ${env}

# filter transaction by game contracts, output in-game-transaction-hashes.csv
python3 get_game_transactions.py

ethereumetl export_receipts_and_logs --transaction-hashes in-game-transaction-hashes.csv --logs-output in-game-logs.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100
ethereumetl extract_token_transfers --logs in-game-logs.csv --output in-game-token-transfers.csv

python3 get_user_transactions.py --env ${env}


