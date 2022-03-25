import csv
import sys

csv.field_size_limit(sys.maxsize)

rent_address = "0xe9e092e46a75d192d9d7d3942f11f116fd2f7ca9"
withdrawl_final_address = "0x94019518f82762bb94280211d19d4ac025d98583"
withdrawl_final_address_new = "0x4a7634c4dd3ae3e3e72f09089807db2f04746741"
generate_shark_address = "0x1f7acc330fe462a9468aa47ecdb543787577e1e7"
auction_address = "0xd78be0b93a3c9d1a9323bca03184accf1a57e548"
withdraw_reward = "0x2df5471b6e25b9dcad2d6169876a9e6a4f5ae882"
mysterious_box = "0xf8dE3211D8652D665647e3DC6E0338713eAf7EbD"

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

in_game_address = set([
    rent_address,
    withdrawl_final_address,
    generate_shark_address,
    auction_address,
    withdraw_reward,
    mysterious_box,
    withdrawl_final_address_new
])

in_game_transaction_hashes =  {}

def get_game_transaction_hashes(date, transaction_file, output):
    output_file = open(output, "w")
    output_file_full_transactions = open(output.replace("-hashes", ""), "w")

    with open(transaction_file, "r") as csv_file:
        data_reader = csv.reader(csv_file)
        for row in data_reader:
            trans = transaction(row)
            if trans.from_address in in_game_address or trans.to_address in in_game_address:
                output_file.write(trans.hash+"\n")
                newrow = ','.join(row)
                output_file_full_transactions.write(newrow+"\n")
    output_file.close()
    output_file_full_transactions.close()

if __name__ == "__main__":
    args = sys.argv[1:]
    date = args[0]
    transaction_file = args[1]
    output_file = args[2]
    get_game_transaction_hashes(date, transaction_file, output_file)
