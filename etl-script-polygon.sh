if [ -z "$1" ]
then
      echo "need date input, e.g. bash scripts.sh 2022-01-01"
      exit 0
fi

range=$(ethereumetl get_block_range_for_date -d $1 --provider-uri https://rpc.ankr.com/polygon/)
rangeArr=(${range//,/ })
echo "Block range for $1: $range"
echo "Getting transactions"
mkdir $1
#touch $1/blockrange-${rangeArr[0]}-${rangeArr[1]}.csv
#ethereumetl export_blocks_and_transactions --start-block ${rangeArr[0]} --end-block ${rangeArr[1]} --transactions-output $1/transactions.csv --provider-uri https://rpc.ankr.com/polygon/ --max-workers 5 --batch-size 10 

# filter transaction by game contracts, output in-game-transaction-hashes.csv
#echo "Getting game transactions"
#python3 get_game_transactions-zed-run.py $1 $1/transactions.csv $1/in-game-transaction-hashes.csv

# Clean up transactions.csv to save disk space
#head -n 2 $1/transactions.csv > $1/transaction-snapshot.csv
#tail -n 1 $1/transactions.csv >> $1/transaction-snapshot.csv
#
#rm $1/transactions.csv

echo "Getting transfers and logs"
#ethereumetl export_receipts_and_logs --transaction-hashes $1/in-game-transaction-hashes.csv --logs-output $1/in-game-logs.csv --provider-uri https://rpc.ankr.com/polygon/ --max-workers 1 --batch-size 1
ethereumetl export_receipts_and_logs --transaction-hashes $1/in-game-transaction-hashes.csv --logs-output $1/in-game-logs.csv --provider-uri https://polygon-mainnet.infura.io/v3/4f8254909eeb42d8bd99107f83ac048c --max-workers 5 --batch-size 100
ethereumetl extract_token_transfers --logs $1/in-game-logs.csv --output $1/in-game-token-transfers.csv
