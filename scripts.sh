ethereumetl export_blocks_and_transactions --start-block 14803641 --end-block 14804641 --transactions-output transactions.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100

python3 get_user_transactions.py # to filter transactions by game contracts
# ethereumetl extract_csv_column --input transactions.csv --column hash --output transaction_hashes.csv 

ethereumetl export_receipts_and_logs --transaction-hashes in-game-transaction_hashes.csv --logs-output in-game-logs.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100

python3 get_user_transactions.py 
# ethereumetl extract_token_transfers --logs in-game-logs.csv --output in-game-token-transfers.csv

# ethereumetl export_traces  --start-block 14662915 --end-block 14672915 --output traces.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100

