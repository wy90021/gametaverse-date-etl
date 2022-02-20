d=2021-12-16
while [ "$d" != 2022-02-16 ]; do 
  echo $d
  range=$(ethereumetl get_block_range_for_date -d $d --provider-uri https://bsc-dataseed.binance.org/)
  rangeArr=(${range//,/ })
  echo "Block range for $d: $range"
  ethereumetl export_blocks_and_transactions --start-block ${rangeArr[0]} --end-block ${rangeArr[1]} --transactions-output $d/transactions.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 10 

  # filter transaction by game contracts, output in-game-transaction-hashes.csv
  echo "Get Transaction IDs"
  python3 get_game_transactions.py $d $d/transactions.csv $d/in-game-transaction-hashes.csv

  rm $d/transactions.csv
  d=$(date -I -d "$d + 1 day")
done
