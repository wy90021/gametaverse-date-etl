import csv
import sys
# from web3 import Web3
# import time, json
import subprocess
from pprint import pprint
import boto3

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
    info = {}

    def __init__(self, row):
        self.hash = row[0]
        self.block_number = row[3]
        self.from_address = row[5]
        self.to_address = row[6]
        self.value = row[7]
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


class log:
    transaction_hash = ""
    block_number = 0
    address  = ""
    data = ""
    data_dec = 0
    data_dec_trim = 0

    def __init__(self, row):
        self.transaction_hash = row[1]
        self.block_number = row[4]
        self.address = row[5]
        self.data = row[6]
        try: 
            self.data_dec = int(self.data, 16)
            data_dec_trim_str = str(self.data_dec).strip("0")
            # self.data_dec_trim = int(data_dec_trim_str) / 10 ** (len(data_dec_trim_str) - 2)
            self.data_dec_trim = decode_hex_value(self.data)

        except ValueError:
            print("cannot decode value: " + self.data)
        self.topics = row[7].split(',')
    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )


in_game_address = set([
    rent_address,
    withdrawl_final_address,
    generate_shark_address,
    auction_address,
    withdraw_reward,
    sea_token_addr
])

in_game_transaction_hashes =  {}

def decode_hex_value(hex): 
    dec_str = str(int(hex, 16))
    i = len(dec_str) - 1
    while i >= 0 and dec_str[i] == '0':
        i = i - 1
    numberofZero = len(dec_str) - i - 1
    if numberofZero > 18:
        return int(dec_str[0:len(dec_str) - 18])
    else:
        return int(dec_str[0:i+1]) / 10 ** (i - 1)



def get_game_transaction_hashes() :
    output_file = open("in-game-transaction-hashes.csv", "w")
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('gametaverse-starsharks-transactions')
    with open("transactions.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        for row in data_reader:
            trans = transaction(row)
            if trans.from_address in in_game_address or trans.to_address in in_game_address:
                # Upload to Dynamo
                # table.put_item(
                #     Item={
                #         'BlockNumber': int(trans.block_number),
                #         'TransactionHash': trans.hash,
                #         'info':  trans.info
                #     })
                output_file.write(trans.hash+"\n")
    output_file.close()

def main():
    get_game_transaction_hashes()

if __name__ == "__main__":
    main()
