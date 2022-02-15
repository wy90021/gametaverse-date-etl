if [ -z "$1" ]
then
      echo "need date and range input, e.g.bash etl-script-range.sh 2022-01-01 12177266 12205036"
      exit 0
fi

mkdir $1
touch $1/blockrange-$2-$3.csv
ethereumetl export_blocks_and_transactions --start-block $2 --end-block $3 --transactions-output $1/transactions-$2-$3.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 1 --batch-size 10

# filter transaction by game contracts, output in-game-transaction-hashes.csv
echo "Get Transaction IDs"
python3 get_game_transactions.py $1 $1/transactions-$2-$3.csv $1/in-game-transaction-hashes-$2-$3.csv

# Clean up transactions.csv to save disk space
head -n 2 $1/transactions-$2-$3.csv > $1/transaction-snapshot-$2-$3.csv
tail -n 1 $1/transactions-$2-$3.csv >> $1/transaction-snapshot-$2-$3.csv

rm $1/transactions-$2-$3.csv

ethereumetl export_receipts_and_logs --transaction-hashes $1/in-game-transaction-hashes-$2-$3.csv --logs-output $1/in-game-logs-$2-$3.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 1 --batch-size 10
ethereumetl extract_token_transfers --logs $1/in-game-logs-$2-$3.csv --output $1/in-game-token-transfers-$2-$3.csv


ethereumetl export_blocks_and_transactions --start-block 13524255 --end-block 13538941 --transactions-output 2021-12-16/transactions-13524255-13538941.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 1 --batch-size 10
