date=$(yesterday 00:00 '+%Y-%m-%d')
bash daily.sh $date > ~/cronlogs/$date.log
