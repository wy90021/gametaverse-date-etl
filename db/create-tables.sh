# aws dynamodb create-table \
#     --table-name gametaverse-starsharks-transactions \
#     --attribute-definitions \
#         AttributeName=BlockNumber,AttributeType=N \
#         AttributeName=TransactionHash,AttributeType=S \
#     --key-schema \
#         AttributeName=BlockNumber,KeyType=HASH \
#         AttributeName=TransactionHash,KeyType=RANGE \
#     --provisioned-throughput \
#         ReadCapacityUnits=10,WriteCapacityUnits=5 \
#     --table-class STANDARD \
#     --endpoint-url=http://localhost:8000

# aws dynamodb create-table \
#     --table-name gametaverse-starsharks-logs \
#     --attribute-definitions \
#         AttributeName=TransactionHash,AttributeType=S \
#         AttributeName=LogIndex,AttributeType=N \
#     --key-schema \
#         AttributeName=TransactionHash,KeyType=HASH \
#         AttributeName=LogIndex,KeyType=RANGE \
#     --provisioned-throughput \
#         ReadCapacityUnits=10,WriteCapacityUnits=5 \
#     --table-class STANDARD \
#     --endpoint-url=http://localhost:8000

aws dynamodb delete-table --table-name gametaverse-starsharks-transactions --endpoint-url=http://localhost:8000
aws dynamodb delete-table --table-name gametaverse-starsharks-logs --endpoint-url=http://localhost:8000
aws dynamodb delete-table --table-name gametaverse-starsharks-users --endpoint-url=http://localhost:8000

aws dynamodb create-table \
    --table-name gametaverse-starsharks-token-transfers \
    --attribute-definitions \
        AttributeName=BlockNumber,AttributeType=N \
        AttributeName=LogIndex,AttributeType=N \
    --key-schema \
        AttributeName=BlockNumber,KeyType=HASH \
        AttributeName=LogIndex,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --table-class STANDARD \
    --endpoint-url=http://localhost:8000

# Only transfer logs, value is a list of transfers in the block, use blockNumber = 00000000 as user profile 
aws dynamodb create-table \
    --table-name gametaverse-starsharks-users \
    --attribute-definitions \
        AttributeName=WalletAddress,AttributeType=S \
        AttributeName=BlockNumber,AttributeType=N \
    --key-schema \
        AttributeName=WalletAddress,KeyType=HASH \
        AttributeName=BlockNumber,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --table-class STANDARD \
    --endpoint-url=http://localhost:8000
    # --profile=prod

# aws dynamodb update-item \
#     --table-name gametaverse-starsharks-users \
#     --key '{"WalletAddress":{"S":"0x9fffefef5094db2454ff9ca4e5aa9c3863fc7758"},"BlockNumber":{"N":"14847036"}}' \
#     --update-expression "ADD transfers :c" \
#     --expression-attribute-values '{":c": {"M": {"111":{"M": {"token_address": {"S": "0x26193c7fa4354ae49ec53ea2cebc513dc39a10aa"},"to_address": {"S": "0x90fbb1f88c0f974cbcc925f57b23fca7e798454a"},"from_address": {"S": "0x151e38fa58e26f9e765a9bb49c033842715df4c1"},"value": {"S": "13000000000000000000"},"transaction_hash": {"S": "0x5a5226127543eebdd36f03f2b12ce729ab32852612781e07313d3a662b08dfce"}}}}}}' \
#     --return-values ALL_NEW \
#     --endpoint-url=http://localhost:8000

# aws dynamodb query \
#     --table-name gametaverse-starsharks-users \
#     --key-condition-expression "WalletAddress = :addr" \
#     --expression-attribute-values  '{":addr":{"S":"0x9fffefef5094db2454ff9ca4e5aa9c3863fc7758"}}' \
#     --endpoint-url=http://localhost:8000
