if [ -z "$1" ]
then
      echo "need date input, e.g. bash etl-script.sh 2022-01-01"
      exit 0
fi

range=$(ethereumetl get_block_range_for_date -d $1 --provider-uri https://bsc-dataseed.binance.org/)
rangeArr=(${range//,/ })
echo "Block range for $1: $range"
output=rawdata/$1/transactions.csv
finaloutput=rawdata/$1/in-game-token-transfers.csv

if [ -f "$finaloutput" ]; then
    echo "$finaloutput exists."
    exit
fi
echo "Getting transactions"
ethereumetl export_blocks_and_transactions --start-block ${rangeArr[0]} --end-block ${rangeArr[1]} --transactions-output $output --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 10 

# filter transaction by game contracts, output in-game-transaction-hashes.csv
echo "Getting game transactions"
python3 get_game_transactions.py $1 rawdata/$1/transactions.csv rawdata/$1/in-game-transaction-hashes.csv

# Clean up transactions.csv to save disk space
head -n 2 rawdata/$1/transactions.csv > rawdata/$1/transaction-snapshot.csv
tail -n 1 rawdata/$1/transactions.csv >> rawdata/$1/transaction-snapshot.csv

rm rawdata/$1/transactions.csv

echo "Getting transfers and logs"
ethereumetl export_receipts_and_logs --transaction-hashes rawdata/$1/in-game-transaction-hashes.csv --logs-output rawdata/$1/in-game-logs.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100
ethereumetl extract_token_transfers --logs rawdata/$1/in-game-logs.csv --output rawdata/$1/in-game-token-transfers.csv
