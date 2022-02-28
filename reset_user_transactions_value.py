import csv
import sys
from dynamodbclient import *
import json

csv.field_size_limit(sys.maxsize)


rent_address = "0xe9e092e46a75d192d9d7d3942f11f116fd2f7ca9"
withdrawl_final_address = "0x94019518f82762bb94280211d19d4ac025d98583"
generate_shark_address = "0x1f7acc330fe462a9468aa47ecdb543787577e1e7"
auction_address = "0xd78be0b93a3c9d1a9323bca03184accf1a57e548"
sea_token_addr = "0x26193c7fa4354ae49ec53ea2cebc513dc39a10aa"
withdraw_reward = "0x2df5471b6e25b9dcad2d6169876a9e6a4f5ae882"
nft_address = "0x416f1d70c1c22608814d9f36c492efb3ba8cad4c"
game_wallet = "0x0000000000000000000000000000000000000000"

class transfer:
    def __init__(self, row):
        self.token_address = row[0] 
        self.from_address = row[1]
        self.to_address = row[2] 
        self.value = row[3]
        self.transaction_hash = row[4]
        self.log_index = row[5]
        self.block_number = row[6]
        self.decoded_value = self.value
        if self.token_address == sea_token_addr: 
            self.decoded_value = int(self.value) / int(1000000000000000000)
        self.info = {
            'value': str(self.decoded_value),
            'transaction_hash': self.transaction_hash,
            'block_number': self.block_number,
            'log_index': self.log_index,
        }
    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    def toMap(self): 
        return self.info

in_game_address = set([
    rent_address,
    withdrawl_final_address,
    generate_shark_address,
    auction_address,
    withdraw_reward,
    nft_address,
    game_wallet,
    sea_token_addr
])

def getTransferID(blockNumber, logIndex):
    return int(blockNumber)*10000 + int(logIndex)

def getBlockTimestamp(block_file): 
    block_timestamp = {}
    with open(block_file, "r") as csv_file:
        data_reader = csv.reader(csv_file)
        csv_file.readline()
        for row in data_reader:
            block_timestamp[row[0]] = row[16]
    return block_timestamp

def update_user_transctions(env, transfer_file, block_file):
    block_timestamps = getBlockTimestamp(block_file)
    dynamodb = getDynamoDBClient(env)
    if dynamodb is None:
        sys.exit("Can't configure dynamoDB client")
    table_user_transfer = dynamodb.Table('gametaverse-user-transfer')

    with open(transfer_file, "r") as csv_file:
        data_reader = csv.reader(csv_file)
        csv_file.readline()
        for row in data_reader:
            transfer_log = transfer(row)
            transferID = getTransferID(transfer_log.block_number, transfer_log.log_index)
            timestamp = block_timestamps[transfer_log.block_number]
            transfer_log.timestamp = timestamp
            transfer_log.transferID = transferID
            if transfer_log.from_address not in in_game_address:
                upload_user_transfer(table_user_transfer, transfer_log.from_address, transfer_log)
            if transfer_log.to_address not in in_game_address:
                upload_user_transfer(table_user_transfer, transfer_log.to_address, transfer_log)

def upload_user_transfer(table_user_transfer, user, transfer):
    table_user_transfer.update_item(
        Key={
            'WalletAddress': user,
            'TransferID': transfer.transferID
        },
        UpdateExpression="set #v=:v",
        ExpressionAttributeNames={
            '#v': "Value",
        },
        ExpressionAttributeValues={
            ':v': transfer.info["value"],
        },
    )


def main(env,transfer_file, block_file):
    update_user_transctions(env, transfer_file, block_file)

if __name__ == "__main__":
    args = sys.argv[1:]
    env = "local"
    if len(args) > 1 and args[0] == "--env" and args[1] == "prod":
        env = "prod"
    transfer_file = args[2]
    block_file = args[3]
    main(env, transfer_file, block_file)
