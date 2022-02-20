if [ -z "$1" ]
then
      echo "need date and env input, e.g. bash block-script.sh 2022-01-01 prod"
      exit 0
fi
d=$1
env="local"
if [ -z "$2" ]
then
      echo "need date and env input, e.g. bash block-script.sh 2022-01-01 prod"
      exit 0
fi
env=$2
echo $d-$env
range=$(ethereumetl get_block_range_for_date -d $d --provider-uri https://bsc-dataseed.binance.org/)
rangeArr=(${range//,/ })
echo "Block range for $d: $range"
mkdir $d
touch $d/blockrange-${rangeArr[0]}-${rangeArr[1]}.csv
ethereumetl export_blocks_and_transactions --start-block ${rangeArr[0]} --end-block ${rangeArr[1]} --blocks-output $d/blocks.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100 
python3 populate_blocks.py --env $env $d/blocks.csv
