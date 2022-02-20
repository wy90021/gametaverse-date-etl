import json
import csv
import requests

def get_starsharks_mysterious_transfers():
    transfers = [['sender_address', 'tx_hash', 'timestamp']]
    headers = {'content-type': 'application/json'}
    url_template = 'https://api.covalenthq.com/v1/56/address/0xf8dE3211D8652D665647e3DC6E0338713eAf7EbD/transactions_v2/?page-number=%d&page-size=1000&key=ckey_601de56b310e44aabef8b30f938'
    page_number = 0
    while True:
        url = url_template % page_number
        transactions_json =requests.get(url, headers=headers).text
        items = json.loads(transactions_json)['data']['items']
        if not items:
            break
        for i, item in enumerate(items):
            if i == 0:
                print(item)
            for log_event in item['log_events']:
                decoded_log_event = log_event['decoded']
                if decoded_log_event and decoded_log_event['name'] == 'Transfer':
                    transfers.append([log_event['sender_address'], log_event['tx_hash'], log_event['block_signed_at']])
        page_number += 1
    with open("starsharks-mysterious-box-transfers.csv","w") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(transfers)
    print("done")

def main():
    transctions_json = get_starsharks_mysterious_transfers()


if __name__ == "__main__":
    main()