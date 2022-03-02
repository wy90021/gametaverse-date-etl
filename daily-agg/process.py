import csv
import sys
import json
import os 
import io

rent_contract = "0xe9e092e46a75d192d9d7d3942f11f116fd2f7ca9"
auction_contract = "0xd78be0b93a3c9d1a9323bca03184accf1a57e548"
generate_shark_contract = "0x1f7acc330fe462a9468aa47ecdb543787577e1e7"
mystery_box_contract = "0xf8dE3211D8652D665647e3DC6E0338713eAf7EbD"
auction_sell_fee_contract = "0x0e3089db5f6a9f0a6550818d1dc274da9f73d4c8"
sea_token = "0x26193c7fa4354ae49ec53ea2cebc513dc39a10aa"
shark_nft = "0x416f1d70c1c22608814d9f36c492efb3ba8cad4c"

withdrawl_final_address = "0x94019518f82762bb94280211d19d4ac025d98583"  
withdraw_reward = "0x2df5471b6e25b9dcad2d6169876a9e6a4f5ae882" # SSS token

game_wallet = "0x0000000000000000000000000000000000000000"

new_user_file = "new_user_time.json"
summary_file = "summary.json"
user_action_file = "user_actions.json"

action_auction_buy = "auction_buy_NFT"
action_auction_sell = "auction_sell_NFT"
action_auction_buy_sea = "auction_buy_SEA"
action_auction_sell_sea = "auction_sell_SEA"
action_buy = "buy_NFT"
action_buy_sea = "buy_SEA"
action_withdrawl_sea = "withdrawl_SEA"

action_lend = "lend_rent_SEA"
action_rent = "rent_shark_SEA"
action_mystery_box = "mystery_box_NFT"

in_game_address = set([
    rent_contract,
    withdrawl_final_address,
    generate_shark_contract,
    auction_contract,
    withdraw_reward,
    sea_token,
    game_wallet,
    mystery_box_contract,
    auction_sell_fee_contract
])

class transaction:
    hash = ""
    block_number = ""
    from_address  = ""
    to_address = ""
    value = 0
    def __init__(self, row):
        self.hash = row[0]
        self.block_number = row[3]
        self.from_address = row[5]
        self.to_address = row[6]
        self.value = row[7]
        self.timestamp = row[11]
        self.input = row[10]
    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    def toMap(self): 
        return {
            'hash': self.hash,
            'block_number': self.block_number,
            'timestamp': self.timestamp,
            'from_address': self.from_address,
            'to_address': self.to_address,
            'value': self.value,
            'input': self.input,
        }

class transfer:
    timestamp = 0
    def __init__(self, row):
        self.token_address = row[0] 
        self.from_address = row[1]
        self.to_address = row[2] 
        self.value = row[3]
        self.transaction_hash = row[4]
        self.log_index = row[5]
        self.block_number = row[6]
        if self.token_address == sea_token: 
            self.value = int(self.value) / int(1000000000000000000)
    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

class user_action:
    action = ""
    value = ""
    trans_hash = ""
    def __init__(self, action, value, hash):
        self.action = action
        self.value = value
        self.trans_hash = hash
    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


def getBlockTimestamp(block_file): 
    block_timestamp = {}
    with open(block_file, "r") as csv_file:
        data_reader = csv.reader(csv_file)
        csv_file.readline()
        for row in data_reader:
            block_timestamp[row[0]] = row[16]
    return block_timestamp

def process(date): 
    transfer_file_path = "../starsharks/"+date+"/in-game-token-transfers.csv"
    block_file_path = "../starsharks/"+date+"/blocks.csv"
    transaction_file_path = "../starsharks/"+date+"/in-game-transaction.csv"

    block_timestamps = getBlockTimestamp(block_file_path)
    transaction_map = load_transactions(transaction_file_path)
    active_user = set()
    # existing_user = {}
    existing_user = get_existing_users()
    sea_volume = 0.0
    rent_shark_volume = 0
    auction_shark_volume = 0
    buy_shark_volume = 0
    create_shark_volume = 0
    new_user = {}
    user_actions = {} # userAddr <> []action
    with open(transfer_file_path, "r") as csv_file:
        data_reader = csv.reader(csv_file)
        csv_file.readline()
        for row in data_reader:
            transfer_log = transfer(row)
            timestamp = block_timestamps[transfer_log.block_number]
            transfer_log.timestamp = timestamp
            if transfer_log.from_address not in in_game_address:
                active_user.add(transfer_log.from_address)
                if transfer_log.from_address not in existing_user:
                    new_user[transfer_log.from_address] = date
            if transfer_log.to_address not in in_game_address:
                active_user.add(transfer_log.to_address)
                if transfer_log.to_address not in existing_user:
                    new_user[transfer_log.to_address] = date
            if transfer_log.token_address == sea_token: 
                sea_volume += transfer_log.value
                trans = transaction_map[transfer_log.transaction_hash]
                if trans is None:
                    print("cannot find transaction: " + transfer_log.transaction_hash)
                contract = trans.to_address
                if  contract == rent_contract: 
                    rent_shark_volume = rent_shark_volume + 1
                    # print("rent shark: " + transfer_log)
                    add_user_action(user_actions, transfer_log.from_address, action_lend, transfer_log.value, transfer_log.transaction_hash)
                    add_user_action(user_actions, transfer_log.to_address, action_rent, transfer_log.value, transfer_log.transaction_hash)
                elif  contract == auction_contract: 
                    add_user_action(user_actions, transfer_log.from_address, action_auction_buy_sea, transfer_log.value, transfer_log.transaction_hash)
                    add_user_action(user_actions, transfer_log.to_address, action_auction_sell_sea, transfer_log.value, transfer_log.transaction_hash)
                elif contract == generate_shark_contract:
                    add_user_action(user_actions, transfer_log.to_address, action_buy_sea, transfer_log.value, transfer_log.transaction_hash)
                elif contract == withdrawl_final_address:
                    add_user_action(user_actions, transfer_log.to_address, action_withdrawl_sea, transfer_log.value, transfer_log.transaction_hash)
            if transfer_log.token_address == shark_nft:
                trans = transaction_map[transfer_log.transaction_hash]
                if trans is None:
                    print("cannot find transaction: " + transfer_log.transaction_hash)
                contract = trans.to_address
                if  contract == auction_contract: 
                    auction_shark_volume = auction_shark_volume + 1
                    add_user_action(user_actions, transfer_log.from_address, action_auction_sell, transfer_log.value, transfer_log.transaction_hash)
                    add_user_action(user_actions, transfer_log.to_address, action_auction_buy, transfer_log.value, transfer_log.transaction_hash)
                elif contract == generate_shark_contract:
                    create_shark_volume = create_shark_volume + 1
                    add_user_action(user_actions, transfer_log.to_address, action_buy, transfer_log.value, transfer_log.transaction_hash)
                elif contract == mystery_box_contract:
                    buy_shark_volume = buy_shark_volume + 1
                    add_user_action(user_actions, transfer_log.to_address, action_mystery_box, transfer_log.value, transfer_log.transaction_hash)
                else: 
                    print("unknown type tansfers" + transfer_log)
    update_existing_user(existing_user, new_user)
    new_user = set()
    existing_user = get_existing_users()
    for user in existing_user:
        if existing_user[user] == date:
            new_user.add(user)

    generate_result(date, active_user, sea_volume, auction_shark_volume, create_shark_volume,rent_shark_volume,buy_shark_volume, user_actions, new_user)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
def obj_dict(obj):
    return obj.__dict__

def generate_result(date, active_user, sea_volume, auction_shark_volume, create_shark_volume,rent_shark_volume,buy_shark_volume, user_actions, new_user):
    script_dir = os.path.dirname(__file__)
    dir = os.path.join(script_dir, date)
    summary_file_path = os.path.join(dir, summary_file)
    user_action_path = os.path.join(dir, user_action_file)

    summary = {
        'active_user': active_user,
        'sea_volume': sea_volume,
        'auction_shark_volume': auction_shark_volume,
        'create_shark_volume': create_shark_volume,
        'rent_shark_volume': rent_shark_volume,
        'buy_shark_volume': buy_shark_volume,
        'new_user': new_user, 
    }

    if not os.path.isdir(dir): 
        os.mkdir(os.path.join(script_dir, date), 0o666)
    with io.open(summary_file_path, 'w') as outfile:
        outfile.write(json.dumps(summary,default=set_default))
    with io.open(user_action_path, 'w') as outfile:
        outfile.write(json.dumps(user_actions, default=obj_dict))

def update_existing_user(existing_user, new_user):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, new_user_file)
    existing_user.update(new_user)
    with open(file_path, 'w') as outfile:
        json.dump(existing_user, outfile)

def add_user_action(user_actions, user_addr, action, value, trans_hash):
    if user_addr in in_game_address:
        return
    if user_addr in user_actions:
        user_actions[user_addr].append(user_action(action, value, trans_hash))
    else:
        user_actions[user_addr] = [user_action(action, value,trans_hash)]

def get_existing_users(): 
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, new_user_file)
    f = open(file_path)
    data = json.load(f)
    f.close()
    return data

def load_transactions(transaction_file_path): 
    transaction_map = {}
    with open(transaction_file_path, "r") as csv_file:
        data_reader = csv.reader(csv_file)
        for row in data_reader:
            trans = transaction(row)
            transaction_map[trans.hash] = trans
    return transaction_map

if __name__ == "__main__":
    args = sys.argv[1:]
    date = args[0]
    process(date)
