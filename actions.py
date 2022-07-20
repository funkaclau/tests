import json
import requests

from classes import UserDecoder, MarketDecoder
from settings import ENTRYPOINT, FILE_TX, RECIPIENT, MEMO, LIMIT, CALORIES_AMOUNT, PATH_USERFILES, PATH_OTHERFILES


def is_not_able_to_move(name, d, c):
    """Check if the collector is able to make a move.
    Receives
        name:   name of the Telegram user;
        d:      json data;
        c:      json data of particular collector.
    Returns
        String with the reason why collector can't move. Or None if he is able to move.
    """
    # Is overburdened
    if len(c['inv']) > c['maxinv']:
        return f"@{name}, your Collector {c['number']} is currently overburdened.\n" \
               f"This means he has more inventory than what he can carry. His current maximum is 3 items. \n " \
               f"Use the command /drop <collector number> <item you want to drop>\n\n" \
               f"If your collector has a Teleportal 🔮 equipped, then you can use:\n" \
               f"/teleport <Collector Number> to withdraw and receive your rewards next Monday"
    # Has no actions left
    if c['actions'] >= c['actionsMax']:
        return f"Dear @{name}, your Collector {c['number']} is too tired to act again this week!\n" \
               f"Try again next week!!"
    # Has not enough energy
    if d['foodBank'] < 45 or d['foodBank'] < 50 and not c['gear']['boots']:
        return f"Dear @{name}, your Collector {c['number']} " \
               f"don't have enough energy in the Food Bank to perform this task."


def check_boots(name, c):
    # Has boots
    if c["gear"]["boots"]:
        print("Boots discount")
        return f"🥾=✅\n\n" \
               f"@{name}, your Collector {c['number']} has a slight discount by having boots 🥾\n" \
               f"Used less than 50 Calories (from Food Bank)."
    # Has no boots
    else:
        return f"🥾=❌\n\n" \
               f"@{name}, your Collector {c['number']} used 50 energy (from Food Bank) to perform this task."


def load_from_market():
    with open(f"{PATH_OTHERFILES}market.json", "r") as f:
        data = json.load(f, cls=MarketDecoder)
    return data


def save_to_market(marketData):
    with open(f"{PATH_OTHERFILES}market.json", "w") as f:
        data = json.dumps(marketData, indent=4)
        f.write(data)


def load_from_userfile(name):
    with open(f"{PATH_USERFILES}{name}.json", "r") as f:
        data = json.load(f, cls=UserDecoder)
    return data


def save_to_userfile(data, name):
    with open(f"{PATH_USERFILES}{name}.json", "w") as f:
        dataS = json.dumps(data, indent=4)
        f.write(dataS)


def get_transfers(sender, recipient, memo, limit):
    payload = {
        "sender": sender,
        "recipient": recipient,
        "memo": memo,
        "limit": limit,
    }
    response = requests.get(ENTRYPOINT, params=payload)
    return response.json()


def tx_not_in_file(filename, tx_id):
    """
    Checks if transaction hash is already in the file.
    Arguments:
        filename: self explanatory
        tx_id: hash of a transaction.
    Returns:
        Returns True if the TX hash wasn't found in the file.
        Returns False, if given TX hash is found in the file.
    """
    with open(filename) as file:
        found = any(tx_id == line.strip() for line in file)
    return not found


def count_calories(wallet_address):
    """
    Calculates the amount of calories.
    Arguments:
        wallet_address: wallet address of the sender
    Returns:
        Amount of calories from the last transaction
    """
    last_transfers = get_transfers(wallet_address, RECIPIENT, MEMO, LIMIT)
    calories = 0
    for transfer in last_transfers["data"]:
        tx_id = transfer["txid"]

        if tx_not_in_file(FILE_TX, tx_id):
            for asset in transfer["assets"]:
                calories += CALORIES_AMOUNT.get(asset["template"]["template_id"], 0)
            with open(FILE_TX, "a") as file:
                file.write(tx_id + "\n")

    return calories


def stashResources(data, name, itemNu, item, key):
    while itemNu > 0:
        data["stash"]["stashinv"].remove(item)
        data["stash"]["stashmissing"][key + "missing"] -= 1
        itemNu -= 1
    save_to_userfile(data, name)


def cResources(d, data, name, itemNu, item, key):
    while itemNu > 0:
        d["inv"].remove(item)
        data["stash"]["stashmissing"][key + "missing"] -= 1
        itemNu -= 1
    save_to_userfile(data, name)
