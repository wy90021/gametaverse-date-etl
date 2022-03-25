aws dynamodb create-table \
    --table-name gametaverse-starsharks-transfer \
    --attribute-definitions \
        AttributeName=TokenAddress,AttributeType=S \
        AttributeName=TransferID,AttributeType=N \
        AttributeName=c,AttributeType=S \
        AttributeName=ToAddress,AttributeType=S \
    --key-schema \
        AttributeName=TokenAddress,KeyType=HASH \
        AttributeName=TransferID,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --table-class STANDARD \
    --endpoint-url=http://localhost:8000 \
    --local-secondary-indexes '[
      {
          "IndexName": "FromAddressIndex",
          "KeySchema": [
              {
                  "AttributeName": "TokenAddress",
                  "KeyType": "HASH"
              },
              {
                  "AttributeName": "FromAddress",
                  "KeyType": "RANGE"
              }
          ],
          "Projection": {
              "ProjectionType": "ALL"
          }
      },
      {
          "IndexName": "ToAddressIndex",
          "KeySchema": [
              {
                  "AttributeName": "TokenAddress",
                  "KeyType": "HASH"
              },
              {
                  "AttributeName": "ToAddress",
                  "KeyType": "RANGE"
              }
          ],
          "Projection": {
              "ProjectionType": "ALL"
          }
      }
    ]' 

# Block time
aws dynamodb create-table \
    --table-name gametaverse-block-timestamp \
    --attribute-definitions \
        AttributeName=Chain,AttributeType=S \
        AttributeName=Timestamp,AttributeType=N \
        AttributeName=BlockNumber,AttributeType=N \
    --key-schema \
        AttributeName=Chain,KeyType=HASH \
        AttributeName=Timestamp,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --table-class STANDARD \
    --endpoint-url=http://localhost:8000  \
    --local-secondary-indexes '[
      {
          "IndexName": "BlockNumberIndex",
          "KeySchema": [
              {
                  "AttributeName": "Chain",
                  "KeyType": "HASH"
              },
              {
                  "AttributeName": "BlockNumber",
                  "KeyType": "RANGE"
              }
          ],
          "Projection": {
              "ProjectionType": "ALL"
          }
      }
    ]' 
# user join time
aws dynamodb create-table \
    --table-name gametaverse-user-profile \
    --attribute-definitions \
        AttributeName=WalletAddress,AttributeType=S \
        AttributeName=GameName,AttributeType=S \
    --key-schema \
        AttributeName=WalletAddress,KeyType=HASH \
        AttributeName=GameName,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --table-class STANDARD \
    --endpoint-url=http://localhost:8000

aws dynamodb create-table \
    --table-name gametaverse-user-transfer \
    --attribute-definitions \
        AttributeName=WalletAddress,AttributeType=S \
        AttributeName=TransferID,AttributeType=N \
    --key-schema \
        AttributeName=WalletAddress,KeyType=HASH \
        AttributeName=TransferID,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --table-class STANDARD \
    --endpoint-url=http://localhost:8000
# GameName, Timestamp, TransactionHash, Role, Value, OtherAddr, TokenAddress, 

aws dynamodb create-table \
    --table-name gametaverse-new-user-time \
    --attribute-definitions \
        AttributeName=GameName,AttributeType=S \
        AttributeName=TransferID,AttributeType=N \
    --key-schema \
        AttributeName=GameName,KeyType=HASH \
        AttributeName=TransferID,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --table-class STANDARD \
    --endpoint-url=http://localhost:8000

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
# aws dynamodb create-table \
#     --table-name gametaverse-starsharks-users \
#     --attribute-definitions \
#         AttributeName=WalletAddress,AttributeType=S \
#         AttributeName=BlockNumber,AttributeType=N \
#     --key-schema \
#         AttributeName=WalletAddress,KeyType=HASH \
#         AttributeName=BlockNumber,KeyType=RANGE \
#     --provisioned-throughput \
#         ReadCapacityUnits=10,WriteCapacityUnits=5 \
#     --table-class STANDARD \
#     --endpoint-url=http://localhost:8000
    # --profile=prod

