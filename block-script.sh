
while [ "$d" != 2022-02-14 ]; do 
  echo $d
  range=$(ethereumetl get_block_range_for_date -d $d --provider-uri https://bsc-dataseed.binance.org/)
  rangeArr=(${range//,/ })
  echo "Block range for $d: $range"
  mkdir $d
  touch $d/blockrange-${rangeArr[0]}-${rangeArr[1]}.csv
  ethereumetl export_blocks_and_transactions --start-block ${rangeArr[0]} --end-block ${rangeArr[1]} --blocks-output $d/blocks.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100 

  d=$(date -I -d "$d + 1 day")
done






