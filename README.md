# Set up Dynamodb locally
1. follow https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html
2. run bash db/create-tables.sh, change the script if local dynamoDB port is not 8000

# How to populate tables
1. Run bash scripts.sh, change the --start-block and --end-block if needed
2. check tables by running 
```
aws dynamodb scan --table-name gametaverse-starsharks-transactions --endpoint-url=http://localhost:8000
aws dynamodb scan --table-name gametaverse-starsharks-logs --endpoint-url=http://localhost:8000
aws dynamodb scan --table-name gametaverse-starsharks-users --endpoint-url=http://localhost:8000
```