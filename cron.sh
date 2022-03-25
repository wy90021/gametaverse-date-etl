date=$(date -d "yesterday 13:00" '+%Y-%m-%d')
bash ~/gametaverse-date-etl/daily.sh $date > ~/cronlogs/$date.log
