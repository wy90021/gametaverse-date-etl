import csv
import sys

csv.field_size_limit(sys.maxsize)

def get_game_contract_transctions():
    sea_address = "0x26193c7fa4354ae49ec53ea2cebc513dc39a10aa"
    #sea_address = "0x7568703d0305c26bc8c5f8166a4d23fd9cb75501"
    count = 0
    output_file = open("starsharks-transactions.csv", "w")
    data_writer = csv.writer(output_file)
    with open("transactions.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        #yield next(data_reader)
        for row in data_reader:
            if row[5] == sea_address or row[6] == sea_address:
                data_writer.writerow(row)
                count += 1
                print(count)

    output_file.close()
    print(count)

def main():
    get_game_contract_transctions()

if __name__ == "__main__":
    main()