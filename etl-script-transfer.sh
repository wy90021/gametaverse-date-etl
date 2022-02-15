if [ -z "$1" ]
then
      echo "need date input, e.g. bash scripts.sh 2022-01-01"
      exit 0
fi

range=$(ethereumetl get_block_range_for_date -d $1 --provider-uri https://bsc-dataseed.binance.org/)
rangeArr=(${range//,/ })
echo "Block range for $1: $range"
mkdir $1
touch $1/blockrange-${rangeArr[0]}-${rangeArr[1]}.csv
ethereumetl export_token_transfers --start-block ${rangeArr[0]} --end-block ${rangeArr[1]} --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100 --output $1/token_transfers.csv
