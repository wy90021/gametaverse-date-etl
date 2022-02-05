ethereumetl export_blocks_and_transactions --start-block 14831156 --end-block 14859905 --transactions-output transactions.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100

# filter transaction by game contracts, upload to DynamoDB and output in-game-transaction-hashes.csv
python3 get_game_transactions.py 

ethereumetl export_receipts_and_logs --transaction-hashes in-game-transaction-hashes.csv --logs-output in-game-logs.csv --provider-uri https://bsc-dataseed.binance.org/ --max-workers 5 --batch-size 100
ethereumetl extract_token_transfers --logs in-game-logs.csv --output in-game-token-transfers.csv

python3 get_user_transactions.py 



# -> filter by game contracts 
# 1. query all game transactions by block range
# have to query block by block 
# aws dynamodb query \
#     --table-name gametaverse-starsharks-transactions \
#     --key-condition-expression "BlockNumber = :block" \
#     --expression-attribute-values  '{":block":{"N":"14839683"}}'\
#     --endpoint-url=http://localhost:8000

# 2. query all game transfer logs by block range
# 3. query active users by block range 
# 4. query user spending and earning by block range
# 5. user profile, start date, owned NFTs