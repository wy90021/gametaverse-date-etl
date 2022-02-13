ethereumetl export_blocks_and_transactions --start-block 15089037 --end-block 15090037 --blocks-output blocks.csv --transactions-output transactions.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100 
python3 populate_blocks.py 

# filter transaction by game contracts, upload to DynamoDB and output in-game-transaction-hashes.csv
python3 get_game_transactions.py 

ethereumetl export_receipts_and_logs --transaction-hashes in-game-transaction-hashes.csv --logs-output in-game-logs.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100
ethereumetl extract_token_transfers --logs in-game-logs.csv --output in-game-token-transfers.csv

python3 get_user_transactions.py 


