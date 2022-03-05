import csv
import sys

csv.field_size_limit(sys.maxsize)

earning_spending_address = "0x89aac1f5ccdd54dd8a09e5c858f19a665e4fa32b"
breeding_address = "0x09ae3a4cde10e50b50c5546e48e758868cdce0ae"
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
    earning_spending_address,
    breeding_address
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
