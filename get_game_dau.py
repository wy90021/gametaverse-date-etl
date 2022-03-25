import csv
import sys
from datetime import datetime

csv.field_size_limit(sys.maxsize)

def get_dau(target_date_timestamp):
    date_object = datetime.fromtimestamp(target_date_timestamp)
    unique_address_set = set()
    with open("starsharks-transactions.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader)
        for row in data_reader:
            transaction_date = datetime.fromtimestamp(int(row[11])).date()
            if transaction_date == date_object.date():
                unique_address_set.add((row[5], row[6]))

    #print(unique_address_set)
    print(len(unique_address_set))

def main():
    get_dau(1639649020) #12/16/2021
    get_dau(1639746066) #12/17/2021
    get_dau(1639832466) #12/18/2021
    get_dau(1639918866) #12/19/2021
    get_dau(1642636800) #1/20/2021
    get_dau(1642550400) #1/19/2021

if __name__ == "__main__":
    main()