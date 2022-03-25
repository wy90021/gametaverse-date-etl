import csv
from email import header
import sys
import json

csv.field_size_limit(sys.maxsize)

rent_address = "0xe9e092e46a75d192d9d7d3942f11f116fd2f7ca9"
withdrawl_final_address = "0x94019518f82762bb94280211d19d4ac025d98583"
generate_shark_address = "0x1f7acc330fe462a9468aa47ecdb543787577e1e7"
auction_address = "0xd78be0b93a3c9d1a9323bca03184accf1a57e548"

in_game_address = set([
    rent_address,
    withdrawl_final_address,
    generate_shark_address,
    auction_address,
])

{
    "address": {
            "timestamp": 1666666,
            "transaction_hash": "xxxxxxx"
    }
}

daily_transfers_with_timestamp_file_path = "in-game-token-transfers-with-timestamp-contract.csv"
per_user_join_time_json_file_path = "../per-user-join-time.json"
per_user_join_time = {}

daily_transfers_csv_header = ["token_address", "from_address", "to_address", "value", "transaction_hash", "log_index", "block_number", "timestamp"]

def add_new_user_join_time():
    with open(per_user_join_time_json_file_path, "r") as per_user_join_time_json_file:
        per_user_join_time = json.load(per_user_join_time_json_file)

    with open(daily_transfers_with_timestamp_file_path, "r") as daily_transfers_csv_file:
        data_reader = csv.reader(daily_transfers_csv_file)
        next(data_reader)
        for row in data_reader:
            buyer_address = row[1]
            earner_address = row[2]
            value = float(row[3])
            transaction_hash = row[4]
            block_number = row[6]
            timestamp = row[7]

            if buyer_address in per_user_join_time and per_user_join_time[buyer_address]['timestamp'] > timestamp:
                print("new buyer", buyer_address)
                per_user_join_time[buyer_address] = {
                    'timestamp': timestamp,
                    'transaction_hash': transaction_hash
                }
            elif not buyer_address in per_user_join_time:
                per_user_join_time[buyer_address] = {
                    'timestamp': timestamp,
                    'transaction_hash': transaction_hash
                }

            if earner_address in per_user_join_time and per_user_join_time[earner_address]['timestamp'] > timestamp:
                print("new earner", earner_address)
                per_user_join_time[earner_address] = {
                    'timestamp': timestamp,
                    'transaction_hash': transaction_hash
                }
            elif not earner_address in per_user_join_time:
                per_user_join_time[earner_address] = {
                    'timestamp': timestamp,
                    'transaction_hash': transaction_hash
                }

    with open(per_user_join_time_json_file_path, "w") as per_user_join_time_json_file:
        per_user_join_time_json_file.write(json.dumps(per_user_join_time))

def main():
    add_new_user_join_time()

if __name__ == "__main__":
    main()