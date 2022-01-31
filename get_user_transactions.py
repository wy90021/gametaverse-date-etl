import csv
import sys
# from web3 import Web3
# import time, json
import subprocess
from pprint import pprint

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
    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )


class log:
    transaction_hash = ""
    block_number = ""
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
        # 123000 -> 123
        # 120000 -> 120
    numberofZero = len(dec_str) - i - 1
    if numberofZero > 18:
        return int(dec_str[0:len(dec_str) - 18])
    else:
        return int(dec_str[0:i+1]) / 10 ** (i - 1)



def get_game_transaction_hashes() :
    output_file = open("in-game-transaction-hashes.csv", "w")
    with open("transactions.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        for row in data_reader:
            trans = transaction(row)
            if trans.from_address in in_game_address or trans.to_address in in_game_address:
                output_file.write(trans.hash+"\n")
    output_file.close()


def get_user_transctions():
    user_transactions = {}
    in_game_transactions = {}
    with open("transactions.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        for row in data_reader:
            trans = transaction(row)
            if trans.from_address in in_game_address or trans.to_address in in_game_address:
                in_game_transactions[trans.hash] = trans
    # print(in_game_transactions)

    with open("in-game-logs.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        csv_file.readline()
        for row in data_reader:
            trans_log = log(row)
            
            if trans_log.data_dec_trim == 0:
                print("Invalid value, log: ")
                print(trans_log)
                continue
            if trans_log.topics[0] != transfer_topic:
                print("Log is not for transfer: ")
                print(trans_log)
                continue
            trans = in_game_transactions[trans_log.transaction_hash]
            if trans.from_address in user_transactions.keys():
                user_transactions[trans.from_address] = user_transactions[trans.from_address] + trans_log.data_dec_trim
            else:
                user_transactions[trans.from_address] =  trans_log.data_dec_trim
            if trans.to_address in user_transactions.keys():
                user_transactions[trans.to_address] = user_transactions[trans.to_address] + trans_log.data_dec_trim
            else:
                user_transactions[trans.to_address] =  trans_log.data_dec_trim

    print(user_transactions)


# def check_logs():
#     # bsc = "https://bsc-dataseed.binance.org/"
#     # web3 = Web3(Web3.HTTPProvider(bsc))
#     # print(web3.isConnected())
#     # # web3.eth.get_transaction_receipt('0x80417d222c39b0f02a682783d0b1c632926e7b0caf85879931de35733a6f542f')
#     # web3.HTTPProvider.get

#     subprocess.run("ethereumetl export_receipts_and_logs -p https://bsc-dataseed.binance.org/ -t user.csv --logs-output -")


def main():
    get_game_transaction_hashes()
    get_user_transctions()

if __name__ == "__main__":
    main()


def get_in_game_contract_transaction_logs():
    count = 0
    
    output_writer_map = {}
    output_file_map = {}
    for addr in in_game_address :
        output_file = open(addr+"-logs.csv", "w")
        output_file_map[addr] = output_file
        data_writer = csv.writer(output_file)
        output_writer_map[addr] = data_writer
        # in_game_transaction_hashes[addr] = set()

    # get all in_game_transaction_hashes
    log_list = []
    with open("in-game-logs.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        for row in data_reader:
            address = row[5]
            transaction_hash = row[1]
            if address in in_game_address:
                new_log = log(row)
                log_list.append(new_log)
                output_writer_map[address].writerow(row)
                in_game_transaction_hashes[transaction_hash] = address
    
    output_file = open("all-transactions-logs.csv", "w")
    all_data_writer = csv.writer(output_file)
    pprint(log_list[0])

    with open("in-game-logs.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        for row in data_reader:
            if row[1] in in_game_transaction_hashes:
                all_data_writer.writerow(row)
                count += 1
    
    for addr in output_file_map: 
        output_file_map[addr].close()
    
    output_file.close()
    print(count)