import csv
import sys

csv.field_size_limit(sys.maxsize)

rent_address = "0xe9e092e46a75d192d9d7d3942f11f116fd2f7ca9"
withdrawl_final_address = "0x94019518f82762bb94280211d19d4ac025d98583"
generate_shark_address = "0x1f7acc330fe462a9468aa47ecdb543787577e1e7"
auction_address = "0xd78be0b93a3c9d1a9323bca03184accf1a57e548"
sea_token_addr = "0x26193c7fa4354ae49ec53ea2cebc513dc39a10aa"
withdraw_reward = "0x2df5471b6e25b9dcad2d6169876a9e6a4f5ae882"

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

    def __init__(self, row):
        self.transaction_hash = row[1]
        self.block_number = row[4]
        self.address = row[5]
        self.data = row[6]
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


def get_game_transaction_hashes(date, transaction_file) :
    output_file = open(date+ "/in-game-transaction-hashes.csv", "w")
    with open(transaction_file, "r") as csv_file:
        data_reader = csv.reader(csv_file)
        for row in data_reader:
            trans = transaction(row)
            if trans.from_address in in_game_address or trans.to_address in in_game_address:
                output_file.write(trans.hash+"\n")
    output_file.close()

if __name__ == "__main__":
    args = sys.argv[1:]
    date = args[0]
    transaction_file = args[1]
    get_game_transaction_hashes(date, transaction_file)
