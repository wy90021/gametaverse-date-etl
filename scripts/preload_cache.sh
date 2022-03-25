if [ -z "$1" ]
then
    d=$(date --date="yesterday" +"%Y-%m-%d")
else
    d=$1
fi
echo $d
d7=$(date --date="${d} -8 day" +"%Y-%m-%d")
d31=$(date --date="${d} -31 day" +"%Y-%m-%d")
dorigin='2021-12-16'
service='https://qhvc5to10e.execute-api.us-west-1.amazonaws.com/staging/grafana/query'
for fromdate in $d7 $d31 $dorigin
do 
    for target in 'daus2' 'daily_transaction_volume2' 'user_repurchase_rate2' 'user_actual_active_dates_distribution2' 'user_total_active_dates_distribution2' 'new_user_spending_usd_distribution2' 'new_rentee_spending_usd_distribution2' 'new_rentee_spending_token_distribution2' 'new_purchaser_spending_usd_distribution2' 'new_purchaser_spending_token_distribution2' 'new_hybrider_spending_usd_distribution2' 'new_hybrider_spending_token_distribution2' 'new_user_profit_usd_distribution2' 'new_rentee_profit_usd_distribution2' 'new_rentee_profit_token_distribution2' 'new_purchaser_profit_usd_distribution2' 'new_purchaser_profit_token_distribution2' 'new_hybrider_profit_usd_distribution2' 'new_hybrider_profit_token_distribution2' 'new_user_profitable_days2' 'new_rentee_profitable_days2' 'new_purchaser_profitable_days2' 'new_hybrider_profitable_days2' 'whale_sort_by_gain2' 'whale_sort_by_profit2' 'whale_sort_by_spending2'
    do 
        echo 'preloading '$fromdate-$d $target
        resp=$(curl -X POST $service --data-raw '{
            "targets": [
                {
                    "target": "'$target'"
                }
            ],
            "range": {
                "from": "'$fromdate'T00:00:00.000Z",
                "to": "'$d'T00:00:00.000Z"
            }
        }')
    done
done