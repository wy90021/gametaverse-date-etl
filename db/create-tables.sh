aws dynamodb create-table \
    --table-name gametaverse-starsharks-transactions \
    --attribute-definitions \
        AttributeName=BlockNumber,AttributeType=N \
        AttributeName=TransactionHash,AttributeType=S \
    --key-schema \
        AttributeName=BlockNumber,KeyType=HASH \
        AttributeName=TransactionHash,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --table-class STANDARD \
    --endpoint-url=http://localhost:8000

aws dynamodb create-table \
    --table-name gametaverse-starsharks-logs \
    --attribute-definitions \
        AttributeName=TransactionHash,AttributeType=S \
        AttributeName=LogIndex,AttributeType=N \
    --key-schema \
        AttributeName=TransactionHash,KeyType=HASH \
        AttributeName=LogIndex,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --table-class STANDARD \
    --endpoint-url=http://localhost:8000

aws dynamodb create-table \
    --table-name gametaverse-starsharks-users \
    --attribute-definitions \
        AttributeName=WalletAddress,AttributeType=S \
        AttributeName=TransactionTimestamp,AttributeType=S \
    --key-schema \
        AttributeName=WalletAddress,KeyType=HASH \
        AttributeName=TransactionTimestamp,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --table-class STANDARD \
    --endpoint-url=http://localhost:8000