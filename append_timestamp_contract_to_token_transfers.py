import csv
from email import header
import sys
import json

csv.field_size_limit(sys.maxsize)

rent_address = "0xe9e092e46a75d192d9d7d3942f11f116fd2f7ca9"
withdrawl_final_address = "0x94019518f82762bb94280211d19d4ac025d98583"
generate_shark_address = "0x1f7acc330fe462a9468aa47ecdb543787577e1e7"
auction_address = "0xd78be0b93a3c9d1a9323bca03184accf1a57e548"

in_game_contract_addresses = set([
    rent_address,
    withdrawl_final_address,
    generate_shark_address,
    auction_address,
])

blocks_file_path = "blocks.csv"
in_game_token_transfers_file_path = "in-game-token-transfers.csv"
in_game_logs_file_path = "in-game-new-logs.csv"
in_game_token_transfers_with_timestamp_file_path = "in-game-token-transfers-with-timestamp-contract.csv"
block_timestamp_dict = {}
transaction_hash_contract_dict = {}

daily_transfers_csv_header = ["token_address", "from_address", "to_address", "value", "transaction_hash", "log_index", "block_number"]

def append_timestamp_to_token_transfers():
    count = 0
    output_file = open("in-game-logs.csv", "w")
    data_writer = csv.writer(output_file)
    in_game_transaction_hashes = set()
    with open(blocks_file_path, "r") as blocks_file:
        data_reader = csv.reader(blocks_file)
        next(data_reader)
        for row in data_reader:
            block_number = row[0]
            timestamp = row[16]
            block_timestamp_dict[block_number] = timestamp
    
    with open(in_game_logs_file_path, "r") as in_game_logs_file:
        data_reader = csv.reader(in_game_logs_file)
        next(data_reader)
        for row in data_reader:
            transaction_hash = row[1]
            contract_addres = row[5]
            if contract_addres in in_game_contract_addresses:
                transaction_hash_contract_dict[transaction_hash] = contract_addres
    #print("transaction_hash_contract_dict", transaction_hash_contract_dict)

    with open(in_game_token_transfers_file_path, "r") as in_game_token_transfers_file:
        with open(in_game_token_transfers_with_timestamp_file_path, "w") as in_game_token_transfers_with_timestamp_file:
            data_reader = csv.reader(in_game_token_transfers_file)
            data_writer = csv.writer(in_game_token_transfers_with_timestamp_file, lineterminator='\n')
            all = []
            row = next(data_reader)
            row.append('timestamp')
            row.append('contract_address')
            all.append(row)

            for row in data_reader:
                transaction_hash = row[4]
                contract_addres = transaction_hash_contract_dict[transaction_hash]
                block_number = row[6]
                timestamp = block_timestamp_dict[block_number]
                row.append(timestamp)
                row.append(contract_addres)
                all.append(row)
            data_writer.writerows(all)

def main():
    append_timestamp_to_token_transfers()

if __name__ == "__main__":
    main()