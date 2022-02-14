
import csv
import sys
from dynamodbclient import *

csv.field_size_limit(sys.maxsize)

def populate_blocks(env):
    dynamodb = getDynamoDBClient(env)
    if dynamodb is None:
        sys.exit("Can't configure dynamoDB client")
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
def main(env="local"):
    populate_blocks(env)

if __name__ == "__main__":
    args = sys.argv[1:]
    env = "local"
    if len(args) > 1 and args[0] == "--env" and args[1] == "prod":
        env = "prod"

    main(env)