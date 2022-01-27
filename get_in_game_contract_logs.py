import csv
import sys

csv.field_size_limit(sys.maxsize)

rent_address = "0xe9e092e46a75d192d9d7d3942f11f116fd2f7ca9"
withdrawl_final_address = "0x94019518f82762bb94280211d19d4ac025d98583"
generate_shark_address = "0x1f7acc330fe462a9468aa47ecdb543787577e1e7"
auction_address = "0xd78be0b93a3c9d1a9323bca03184accf1a57e548"

in_game_address = set([
    rent_address,
    withdrawl_final_address,
    generate_shark_address,
    auction_address
])
def get_in_game_contract_transaction_logs():
    count = 0
    output_file = open("in-game-logs.csv", "w")
    data_writer = csv.writer(output_file)
    in_game_transaction_hashes = set()
    with open("logs.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        for row in data_reader:
            if row[5] in in_game_address:
                in_game_transaction_hashes.add(row[1])
    with open("logs.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        for row in data_reader:
            if row[1] in in_game_transaction_hashes:
                data_writer.writerow(row)
                count += 1
                print(count)

    output_file.close()
    print(count)

def main():
    get_in_game_contract_transaction_logs()

if __name__ == "__main__":
    main()