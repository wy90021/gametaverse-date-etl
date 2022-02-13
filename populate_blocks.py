
from cgi import test
import csv
import sys
import boto3

csv.field_size_limit(sys.maxsize)

def populate_blocks():
    # Local
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table_blocks = dynamodb.Table('gametaverse-block-timestamp')
    with open("blocks.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        csv_file.readline()
        for row in data_reader:
            table_blocks.put_item(
                Item={
                    'Chain':  'BSC',
                    'Timestamp': int(row[16]),
                    'BlockNumber': int(row[0]),
                })
def main():
    populate_blocks()

if __name__ == "__main__":
    main()