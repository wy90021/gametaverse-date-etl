ethereumetl export_blocks_and_transactions --start-block 14803641 --end-block 14804641 --transactions-output transactions.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100

# filter transaction by game contracts, upload to DynamoDB and output in-game-transaction-hashes.csv
python3 get_game_transactions.py 

ethereumetl export_receipts_and_logs --transaction-hashes in-game-transaction-hashes.csv --logs-output in-game-logs.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100

python3 get_user_transactions.py 
# ethereumetl extract_token_transfers --logs in-game-logs.csv --output in-game-token-transfers.csv

# ethereumetl export_traces  --start-block 14662915 --end-block 14672915 --output traces.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100

