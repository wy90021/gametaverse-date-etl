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

transfer_topic = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

class transaction:
    hash = ""
    block_number = ""
    from_address  = ""
    to_address = ""
    value = 0
    def __init__(self, row):
        self.hash = row[0]
        self.block_number = row[3]
        self.from_address = row[5]
        self.to_address = row[6]
        self.value = row[7]
        self.timestamp = row[11]
        self.input = row[10]
        self.info = {
            'from_address': self.from_address,
            'to_address': self.to_address,
            'value': self.value,
            'input': row[10],
        }
    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    def toMap(self): 
        return {
            'hash': self.hash,
            'block_number': self.block_number,
            'timestamp': self.timestamp,
            'from_address': self.from_address,
            'to_address': self.to_address,
            'value': self.value,
            'input': self.input,
        }

class log:
    transaction_hash = ""
    block_number = ""
    address  = ""
    data = ""
    data_dec = 0
    log_index = 0
    info = {}
    def __init__(self, row):
        self.log_index = row[0]
        self.transaction_hash = row[1]
        self.block_number = row[4]
        self.address = row[5]
        self.data = row[6]
        try: 
            self.data_dec = int(self.data, 16)
            self.data_dec_trim = int(self.data_dec) / int(1000000000000000000)

        except ValueError:
            print("cannot decode value: " + self.data)
        self.topics = row[7].split(',')
        self.info = {
            'block_number': self.block_number,
            'address': self.address,
            'data': self.data,
            'topics': self.topics,
            'data_dec_trim':  str(self.data_dec_trim)
        }
    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    def toMap(self): 
        return {
            'log_index': self.log_index,
            'address': self.address,
            'data': self.data,
            'topics': self.topics,
            'data_dec_trim': str(self.data_dec_trim)
        }

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

def get_user_transctions(env, transfer_file, block_file):
    block_timestamps = getBlockTimestamp(block_file)
    dynamodb = getDynamoDBClient(env)
    if dynamodb is None:
        sys.exit("Can't configure dynamoDB client")
    table_transfer = dynamodb.Table('gametaverse-starsharks-transfer')
    table_user_profile = dynamodb.Table('gametaverse-user-profile')
    table_new_user = dynamodb.Table('gametaverse-new-user-time')
    
    with open(transfer_file, "r") as csv_file:
        data_reader = csv.reader(csv_file)
        csv_file.readline()
        for row in data_reader:
            transfer_log = transfer(row)
            transferID = getTransferID(transfer_log.block_number, transfer_log.log_index)
            timestamp = block_timestamps[transfer_log.block_number]
            table_transfer.put_item(
                Item={
                    'TokenAddress':  transfer_log.token_address,
                    'TransferID': transferID,
                    'FromAddress': transfer_log.from_address,
                    'ToAddress': transfer_log.to_address,
                    'info':  transfer_log.info,
                    'timestamp': timestamp,
                })
            transfer_log.timestamp = timestamp
            update_if_new_user(table_user_profile, table_new_user, transferID, transfer_log.from_address)
            update_if_new_user(table_user_profile, table_new_user, transferID, transfer_log.to_address)
            # res = add_transfer_to_user_profile(table_user_profile, transfer_log.from_address, transfer_log)
            # print(res)
            # add_transfer_to_user_profile(table_user_profile, transfer_log.to_address, transfer_log)


def update_if_new_user(table_user_profile, table_new_user, transferID, user): 
    user_profile = table_user_profile.get_item(
        Key={
            "WalletAddress": user,
            "GameName": "Starsharks"
        },
    )
    if "Item" in user_profile and user_profile["Item"]["JoinTime"] <= transferID:
        return
    print(user + " is new to Starsharks\n")
    table_user_profile.put_item(
        Item={
            'WalletAddress': user,
            'GameName': 'Starsharks',
            'JoinTime':  transferID,
        },
    )
    table_new_user.put_item(
        Item={
            'GameName': 'Starsharks',
            'TransferID': transferID,
            'User': user,
        }
    )

def add_transfer_to_user_profile(table_user_profile, user, transfer):
    result = table_user_profile.update_item(
        Key={
            'WalletAddress': user,
            'GameName': "Starsharks"
        },
        UpdateExpression="SET Transfers = list_append(Transfers, :i)",
        ExpressionAttributeValues={
            ':i': [json.dumps(transfer)],
        },
        ReturnValues="UPDATED_NEW"
    )
    if result['ResponseMetadata']['HTTPStatusCode'] == 200 and 'Attributes' in result:
        return result['Attributes']['Transfers']

def main(env,transfer_file, block_file):
    get_user_transctions(env, transfer_file, block_file)

if __name__ == "__main__":
    args = sys.argv[1:]
    env = "local"
    if len(args) > 1 and args[0] == "--env" and args[1] == "prod":
        env = "prod"
    transfer_file = args[2]
    block_file = args[3]
    main(env, transfer_file, block_file)
