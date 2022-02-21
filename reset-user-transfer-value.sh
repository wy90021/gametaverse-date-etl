d=2021-12-16
while [ "$d" != 2022-01-21 ]; do 
  echo $d
  python3 reset_user_transactions_value.py --env prod $d/in-game-token-transfers.csv $d/blocks.csv
  d=$(date -I -d "$d + 1 day")
done
  # python3 upload_user_transactions.py --env prod 2022-02-16/in-game-token-transfers.csv 2022-02-16/blocks.csv