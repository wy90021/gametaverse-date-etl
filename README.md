# Set up Dynamodb locally
1. follow https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html
2. run bash db/create-tables.sh, change the script if local dynamoDB port is not 8000

# How to populate tables
1. Run bash scripts.sh, change the --start-block and --end-block if needed
2. check tables by running 
```
aws dynamodb scan --table-name gametaverse-block-timestamp --endpoint-url=http://localhost:8000 --max-items 100
aws dynamodb scan --table-name gametaverse-starsharks-transfer --endpoint-url=http://localhost:8000 --max-items 100
aws dynamodb scan --table-name gametaverse-user-profile --endpoint-url=http://localhost:8000 --max-items 100
aws dynamodb scan --table-name gametaverse-new-user-time --endpoint-url=http://localhost:8000 --max-items 100
```

# Set up env 
sudo apt-get install python3.7
sudo apt-get install pip3
pip3 install ethereum-etl
pip3 install boto3