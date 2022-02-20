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


# How to process a day's data

1. run `bash block-script.sh 2021-12-19` to fetch block data and upload to dynamo
2. run `bash etl-script.sh 2021-12-19` to fetch transfer data and filter by game
3. run `bash dynamo-scripts.sh 2021-12-19 prod` to upload transfer and user data


still need to finish timestamp backfill starting 1-30
then need to start user transfer backfill