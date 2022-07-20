import json
import os
from random import randint
import telebot

from actions import is_not_able_to_move, check_boots, save_to_market, save_to_userfile, load_from_userfile, \
    count_calories, stashResources, cResources, load_from_market
from classes import UserDecoder, MarketDecoder
from settings import RECIPIENT, MEMO

# Read API key
API_KEY = os.environ["API_KEY"]
# Create bot object
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["explore", "e"])
def bot_explore(message):
    name = message.from_user.username
    print(f"{name} {message.text}")
    if len(message.text.split()) == 1:
        bot.send_message(
            message.chat.id,
            f"🚶‍♂️ EXPLORE 🚶‍♂️\n\n"
            f"Explore is the command that allows you to send your Collectors into exploration "
            f"in order to find a random terrain type, with rewards that vary depending on its type.\n\n"
            f"Each exploration will place your collector farther from home up to a maximum "
            f"of 4 Units of Distance.\n\nThis command costs 50 energy, yet this cost can be reduced by or "
            f"offset depending on the equipment held by the collector.\n\n To start exploring with "
            f"a Collector use the command:\n/explore <Collector nr>\nReplace <Collector nr> with the number "
            f"of the collector you want to perform the action with.\n\n Once your collector successfuly "
            f"explores, a new NFT will be added to his inventory.\n\nIn case of doubt use /inv or "
            f"/inv <Collector nr> To find more info.\n\nRemember that in order to redeem the items you "
            f"earned you need to take your collector /home or /teleport 🔮 his items. Alternatively there "
            f"are many ways to use your earnings 'in game', to earn even more. /list will show you all the "
            f"possibilities you have at hand!\n\n"
            f"End of report 🧐",
        )
    elif len(message.text.split()) == 2:
        data = load_from_userfile(name)
        collector_number = int(message.text.split()[1]) - 1
        collector_data = data["collectors"][collector_number]
        reason_found = is_not_able_to_move(name, data, collector_data)
        if reason_found:
            bot.send_message(
                message.chat.id,
                reason_found
            )
            return
        bot.send_message(
            message.chat.id,
            check_boots(name, collector_data)
        )
        data["exploreC"] += 1
        data["collectors"][collector_number]["actions"] += 1
        exploreC(data, message, name)
        locatRoll(collector_data, data, message, name)
    else:
        bot.send_message(
            message.chat.id,
            f"@{name} you are doing something wrong. Try /explore <collector number> \n "
            f"replace <collector number> with a number.",
        )


@bot.message_handler(commands=["search", "s"])
def bot_search(message):
    name = message.from_user.username
    print(f"{name} {message.text}")
    if len(message.text.split()) == 1:
        bot.send_message(
            message.chat.id,
            f"🔍 Search 🔎\n\n"
            f"Search 🔎 is the command that allow you to use your Collectors to search "
            f"their current location to find 2 random items. /search allows you to find more NFT types "
            f"than /explore.\n Please note that you can't use Search 🔎 at Home.\n\nThis command costs 50 "
            f"energy, yet this cost can be reduced, depending on the equipment held by the collector.\n\n"
            f"To start searching with a Collector use the command:\n/search <Collector nr>\n"
            f"Replace <Collector nr> with the number of the collector you want to perform the action with.\n\n"
            f"Once your collector successfully searches 🔎, new NFTs will be added to his inventory.\n\n"
            f"In case of doubt use /inv or /inv <Collector nr> To find more info.\n\n"
            f"Remember that in order to redeem the items you earned you need to take your collector "
            f"/home or /teleport 🔮 his items. Alternatively there are many ways to use your earnings "
            f"'in game', to earn even more. /list will show you all the possibilities you have at hand!\n\n"
            f"End of report 🧐",
        )
    elif len(message.text.split()) == 2:
        data = load_from_userfile(name)
        collector_number = int(message.text.split()[1]) - 1
        collector_data = data["collectors"][collector_number]
        reason_found = is_not_able_to_move(name, data, collector_data)
        if reason_found:
            bot.send_message(
                message.chat.id,
                reason_found
            )
            return
        bot.send_message(
            message.chat.id,
            check_boots(name, collector_data)
        )
        localCheck(collector_data, data, message, name)
    else:
        bot.send_message(
            message.chat.id,
            f"@{name} you are doing something wrong. Try /search <collector number> \n "
            f"replace <collector number> with a number.",
        )


@bot.message_handler(commands=["home", "h"])
def bot_home(message):
    name = message.from_user.username
    print(f"{name} {message.text}")
    if len(message.text.split()) == 1:
        bot.send_message(
            message.chat.id,
            f"🏠 HOME 🏠\n\n"
            f"Home is the place where you need to send your Collectors to in order to withdraw the NFTs you earned "
            f"while playing this game.\n\n Every time you send your Collector Home 🏠, 1 Unit of Distance from Home "
            f"will be deducted and once it reaches 0, your Collector will arrive Home .\n\nThis command costs 50 "
            f"energy, yet this cost can be reduced by or offset depending on the equipment held by the collector.\n\n"
            f"To start moving Home 🏠 with a Collector use the command:\n/home <Collector nr>\nReplace <Collector nr> "
            f"with the number of the collector you want to perform the action with.\n\n Once your collector arrives at "
            f"Home 🏠, the process of withdrawing NFTs gets started. Next Monday after you successfuly reached Home 🏠, "
            f"you will receive your NFTs. \n\nIn case of doubt use /inv or /inv <Collector nr> To find more info. \n"
            f"Alternatively there are many ways to use your earnings 'in game', to earn even more. /list will show you "
            f"all the possibilities you have at hand!\n\n End of report 🧐",
        )
    elif len(message.text.split()) == 2:
        data = load_from_userfile(name)
        collector_number = int(message.text.split()[1]) - 1
        collector_data = data["collectors"][collector_number]
        reason_found = is_not_able_to_move(name, data, collector_data)
        if reason_found:
            bot.send_message(
                message.chat.id,
                reason_found
            )
            return
        bot.send_message(
            message.chat.id,
            check_boots(name, collector_data)
        )
        home(collector_data, data, message, name)
    else:
        bot.send_message(
            message.chat.id,
            f"@{name} you are doing something wrong. Try /home <collector number> \n "
            f"replace <collector number> with a number.",
        )


@bot.message_handler(commands=["inv"])
def bot_inventory(message):
    name = message.from_user.username
    print(f"{name} {message.text}")
    if len(message.text.split()) == 1:
        data = load_from_userfile(name)
        invP(data, message, name)
    elif len(message.text.split()) == 2:
        data = load_from_userfile(name)
        collector_number = int(message.text.split()[1]) - 1
        collector_data = data["collectors"][collector_number]
        inv(collector_data, data, message, name)
    else:
        bot.send_message(
            message.chat.id,
            f"@{name} you are doing something wrong. Try /inv <collector number> \n"
            f"replace <collector number> with a number.",
        )


@bot.message_handler(commands=["drop"])
def bot_drop(message):
    name = message.from_user.username
    print(f"{name} {message.text}")
    if len(message.text.split()) <= 2:
        bot.send_message(
            message.chat.id,
            f"🩸 DROP🩸\n\n"
            f"Drop command allows you to get rid of 1 item inside a Collector Inventory. \n"
            f"Why would you drop one item? Well, there are times your collector may get overburdened and unable "
            f"to act.\n\nWithout a Teleportal 🔮 or a Stash, Drop can be used remove extra weight from "
            f"the collector.\n\nTo use the Command:\n/drop <collector nr> <item nr>\nReplace <Collector nr> "
            f"with the number of the collector you want to perform the action with.\nReplace <item nr> with "
            f"the index nr of the item you want to drop.\n\nIn case of doubt use /inv or /inv <Collector nr> "
            f"To find more info.\n\nRemember that items you drop can never be retrieved, so please use it wisely."
        )
    elif len(message.text.split()) == 3:
        data = load_from_userfile(name)
        collector = int(message.text.split()[1])
        collector_number = collector - 1
        collector_data = data["collectors"][collector_number]
        item_number = int(message.text.split()[2]) - 1
        if len(collector_data['inv']) > item_number:
            bot.send_message(
                message.chat.id,
                f"🩸 DROP🩸\n\n"
                f"Your Collector {collector} successfully dropped {collector_data['inv'][item_number]}",
            )
            del collector_data["inv"][item_number]
            save_to_userfile(data, name)
        else:
            bot.send_message(
                message.chat.id,
                f"Error: nothing to drop",
            )
    else:
        bot.send_message(
            message.chat.id,
            f"@{name} you are doing something wrong. \n\n"
            f"Use /drop <collector number> <number of item in collector inv> or just /drop for more info!",
        )


@bot.message_handler(commands=["chop"])
def bot_chop(message):
    name = message.from_user.username
    print(f"{name} {message.text}")
    if len(message.text.split()) == 1:
        bot.send_message(
            message.chat.id,
            f"🪓 CHOP 🪓\n\n"
            f"Chop allows your collector to use his calories to find wood, rather than a random NFT.\n\n"
            f"To /chop, make sure your collector:\nHas an Axe 🪓 Equipped ✅\nYour Collector Location is "
            f"Forest or Woodland ✅\nHe has enough Calories ✅\n If all this requirements are met, you can:\n\n"
            f"/chop <Collector nr>\nReplace <Collector nr> with the number of the collector you want to Chop with.\n\n"
            f"Once your collector successfuly chops, new NFTs will be added to his inventory.\n\n"
            f"In case of doubt use /inv or /inv <Collector nr> To find more info.\n\n"
            f"Remember that in order to redeem the items you earned you need to take your collector /home "
            f"or /teleport his items. Alternatively there are many ways to use your earnings 'in game', to "
            f"earn even more. /list will show you all the possibilities you have at hand!\n\n End of report 🧐",
        )
    elif len(message.text.split()) == 2:
        data = load_from_userfile(name)
        collector_number = int(message.text.split()[1]) - 1
        collector_data = data["collectors"][collector_number]
        if collector_data["gear"]["axe"]:
            reason_found = is_not_able_to_move(name, data, collector_data)
            if reason_found:
                bot.send_message(
                    message.chat.id,
                    reason_found
                )
                return
            bot.send_message(
                message.chat.id,
                check_boots(name, collector_data)
            )
            localCheckChop(collector_data, data, message, name)
        else:
            bot.send_message(
                message.chat.id,
                f"🪓=❌\n\n@{name}, your Collector {collector_data['number']} doesn't have an axe 🪓 equipped! ❌",
            )
    else:
        bot.send_message(
            message.chat.id,
            f"@{name} you are doing something wrong. Try /chop <collector number> \n"
            f"replace <collector number> with a number. Using just /chop will use your collector 1 by default",
        )


@bot.message_handler(commands=["mine"])
def bot_mine(message):
    name = message.from_user.username
    print(f"{name} {message.text}")
    if len(message.text.split()) == 1:
        bot.send_message(
            message.chat.id,
            f"⛏ MINE ⛏\n\n"
            f"Mine allows your collector to use his calories to find Stones and Ores, rather than a random "
            f"NFT from Rocky Terrains.\n\nTo /mine, make sure your collector:\nHas an Pickaxe ⛏ Equipped ✅\n"
            f"Your Collector Location is Rocky ✅\nHe has enough Calories ✅\n If all this requirements are met, "
            f"you can:\n\n/mine <Collector nr>\nReplace <Collector nr> with the number of the collector you want "
            f"to Mine with.\n\n Once your collector successfuly Mines, new NFTs will be added to his inventory.\n\n"
            f"In case of doubt use /inv or /inv <Collector nr> To find more info.\n\nRemember that in order to "
            f"redeem the items you earned you need to take your collector /home or /teleport his items. Alternatively "
            f"there are many ways to use your earnings 'in game', to earn even more. /list will show you all "
            f"the possibilities you have at hand!\n\n End of report 🧐",
        )
    elif len(message.text.split()) == 2:
        data = load_from_userfile(name)
        collector_number = int(message.text.split()[1]) - 1
        collector_data = data["collectors"][collector_number]
        if collector_data["gear"]["pick"]:
            reason_found = is_not_able_to_move(name, data, collector_data)
            if reason_found:
                bot.send_message(
                    message.chat.id,
                    reason_found
                )
                return
            bot.send_message(
                message.chat.id,
                check_boots(name, collector_data)
            )
            localCheckMine(collector_data, data, message, name)
        else:
            bot.send_message(
                message.chat.id,
                f"⛏=❌\n\n@{name}, your Collector {collector_data['number']} doesn't have a pickaxe ⛏ equipped! ❌",
            )
    else:
        bot.send_message(
            message.chat.id,
            f"@{name}, you are doing something wrong. Try /mine <collector number> \n"
            f"replace <collector number> with a number.",
        )


@bot.message_handler(commands=["teleport", "tp"])
def teleport(message):
    name = message.from_user.username
    print(f"{name} {message.text}")
    if len(message.text.split()) == 1:
        bot.send_message(
            message.chat.id,
            f"🔮 TELEPORTAL 🔮\n\n"
            f"Home is the place where you need to send your Collectors to in order to withdraw the NFTs "
            f"you earned while playing this game., UNLESS... You hold a Teleportal 🔮\n\n By holding a "
            f"teleportal 🔮 with the selected collector, you will be able to redeem his findings without "
            f"the need to return Home to do so.\n\nThis command costs no energy and will output the same "
            f"result of arriving at Home, without the need to move.\n\n To start teleporting items with a "
            f"Collector use the command:\n/teleport <Collector nr>\nReplace <Collector nr> with the number "
            f"of the collector you want to perform the action with.\n\n after your collector Teleports his "
            f"bag, the process of withdrawing NFTs gets started. Next Monday after you successfuly started "
            f"this process, you will receive your NFTs. \n\nIn case of doubt use /inv or /inv <Collector nr> "
            f"To find more info. \nAlternatively there are many ways to use your earnings 'in game', to earn "
            f"even more. /list will show you all the possibilities you have at hand!\n\n End of report 🧐",
        )
    elif len(message.text.split()) == 2:
        data = load_from_userfile(name)
        collector_number = int(message.text.split()[1]) - 1
        collector_data = data["collectors"][collector_number]
        teleportal(collector_data, data, message, name)
    else:
        bot.send_message(
            message.chat.id,
            f"@{name}, you are doing something wrong. Try /teleport <collector number> \n"
            f"replace <collector number> with a number.",
        )


@bot.message_handler(commands=["stashlocation"])
def bot_stashlocation(message):
    name = message.from_user.username
    data = load_from_userfile(name)
    if len(message.text.split()) == 1 and data['stash']['stashlocation'] is False:
        bot.send_message(
            message.chat.id,
            f"Hello @{name}!\n"
            f"With this command you can define in which terrain you will build your stash.\n\n"
            f"Choose well, because you cant change it later...\n\nOnce you have chosen, insert the command:\n"
            f"/stashlocation <terrain type>\n\nReplace <terrain type> with terrain name.\n\nTERRAIN TYPES\n"
            f"Plains\nWoodland\nForest\nRocky\nMuddy\nLake\nBeach\nSwamp\n\nPlease also have in mind that "
            f"choosing a rarer terrain is not advised",
        )
    elif data['stash']['stashlocation'] and len(message.text.split()) == 1:
        bot.send_message(
            message.chat.id,
            f"Hello @{name}, you have already selected a terrain to build your stash.\n"
            f"Stash Location: {data['stash']['stashlocation']}\n\n"
            f"For more info about your Stash use /stash",
        )
    elif len(message.text.split()) == 2 and data['stash']['stashlocation']:
        bot.send_message(
            message.chat.id,
            f"@{name}, you have already selected a terrain to build your stash.",
        )
    elif len(message.text.split()) == 2 and data['stash']['stashlocation'] is False:
        terrain = message.text.split()[1].capitalize()
        terrains = [
            "Plains",
            "Woodland",
            "Forest",
            "Rocky",
            "Muddy",
            "Lake",
            "Beach",
            "Swamp",
        ]
        if terrain in terrains:
            data['stash']['stashlocation'] = terrain
            bot.send_message(
                message.chat.id,
                f"@{name}, you successfully started establishing a Stash at:\n\n\n"
                f"{data['stash']['stashlocation']}!\n\n"
                f"From now on, your collectors at {data['stash']['stashlocation']} will be able to contribute "
                f"to the development of your stash and much more...\nKeep it up, Pixeler",
            )
            save_to_userfile(data, name)
        else:
            bot.send_message(
                message.chat.id,
                f"@{name}, you are doing something wrong. \n\nUse /stashlocation for more info",
            )
    else:
        bot.send_message(
            message.chat.id,
            f"@{name}, you are doing something wrong. \n\nUse /stashlocation for more info",
        )


@bot.message_handler(commands=["stashwood", "sw"])
def stashwood(message):
    name = message.from_user.username
    item = "Plain Wood"
    data = load_from_userfile(name)
    colN = 1
    colNu = int(colN) - 1
    d = data["collectors"][colNu]
    stash = data["stash"]["stashinv"]
    data["stash"]["stashmissing"]["woodmissing"] = data["stash"]["stashmissing"][
        "woodmissing"
    ]
    itemNu = 1
    key = "wood"
    m1 = (
        "@"
        + name
        + " this command makes your collector contribute to the Stash development with "
        + str(itemNu)
        + " "
        + item
        + " 🪵from his inventory.\n\nPlease note that your collector needs to be at "
        + data['stash']['stashlocation']
        + " or Holding Teleportal 🔮 + 1 "
        + item
        + " 🪵 in inventory \n\n use  /stashwood <collector nr> or /stashwood <collector nr> <number> for bulk contribution. \nAlternatively you can contribute with items from your stash: \n /stashwood stash or stashwood stash <nr> for bulk contribution."
    )

    stashOnly = (
        "@"
        + name
        + ", Your Stash only has "
        + str(data["stash"]["stashinv"].count(item))
        + " "
        + item
        + "!\n\n🪵=❌"
    )
    cOnly = (
        "@"
        + name
        + ", Your Collector "
        + str(colN)
        + " only has "
        + str(d["inv"].count(item))
        + " "
        + item
        + "!\n\n🪵=❌"
    )

    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, m1)
    elif len(message.text.split()) == 2:
        if message.text.split()[1] == "stash":
            if item in stash:
                if data["stash"]["stashmissing"]["woodmissing"] == 1:
                    stash.remove(item)
                    data["stash"]["stashmissing"]["woodmissing"] -= 1
                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + ", you  Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🪵 to the Stash creation using your Stash Supply.\n\nCongratz!! \n\nYou just finished gathering all the "
                        + item
                        + " 🪵 to build your Stash Lvl "
                        + str(data["stash"]["stashlevel"] + 1)
                        + "!\n\nChecking for a potential Lvl Up...",
                    )
                    stashLevelCheck(data, message, name)
                elif data["stash"]["stashmissing"]["woodmissing"] > 1:
                    stash.remove(item)
                    data["stash"]["stashmissing"]["woodmissing"] -= 1
                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " you Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🪵 to the Stash creation using your Stash supply. \n\nNow you only need "
                        + str(data["stash"]["stashmissing"]["woodmissing"])
                        + " "
                        + item
                        + " 🪵",
                    )
                else:
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " Your stash doesnt need "
                        + item
                        + " 🪵 for the next level.",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    "@" + name + " Your stash doesnt hold any " + item + "!",
                )
        # from collector INV
        else:
            colN = message.text.split()[1]
            colNu = int(colN) - 1
            d = data["collectors"][colNu]
            if item not in d["inv"]:
                bot.send_message(
                    message.chat.id,
                    "@"
                    + name
                    + ", Your collector has no "
                    + item
                    + " on his inventory\n\n🪵=❌",
                )
            else:
                if d["location"] != data['stash']['stashlocation']:
                    if d["gear"]["tele"] is False:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector is not at  "
                            + data['stash']['stashlocation']
                            + " and also hasn't a Teleportal  🔮 equipped!\n\nTo contribute to the Stash Creation  explore until you find "
                            + data['stash']['stashlocation']
                            + "!",
                        )
                    else:
                        if data["stash"]["stashmissing"]["woodmissing"] == 1:

                            d["inv"].remove(item)
                            data["stash"]["stashmissing"]["woodmissing"] -= 1
                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🪵 to the Stash creation using his Teleportal 🔮. \n\nCongratz!! \n\nYou just finished gathering all the "
                                + item
                                + " 🪵 to build your Stash Lvl "
                                + str(data["stash"]["stashlevel"] + 1)
                                + "!\n\nChecking for a potential Lvl Up...",
                            )
                            stashLevelCheck(data, message, name)

                        elif data["stash"]["stashmissing"]["woodmissing"] > 1:

                            d["inv"].remove(item)
                            data["stash"]["stashmissing"]["woodmissing"] -= 1

                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🪵 to the Stash creation using his Teleportal 🔮. \n\nNow you only need "
                                + str(data["stash"]["stashmissing"]["woodmissing"])
                                + " "
                                + item
                                + " 🪵",
                            )
                        else:
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " Your stash doesnt need "
                                + item
                                + " 🪵 for the next level.",
                            )
                else:
                    if data["stash"]["stashmissing"]["woodmissing"] == 1:

                        d["inv"].remove(item)
                        data["stash"]["stashmissing"]["woodmissing"] -= 1
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🪵 to the Stash creation. \n\nCongratz!! \n\nYou just finished gathering all the "
                            + item
                            + " 🪵 to build your Stash Lvl "
                            + str(data["stash"]["stashlevel"] + 1)
                            + "!\n\nChecking for a potential Lvl Up...",
                        )
                        stashLevelCheck(data, message, name)

                    elif data["stash"]["stashmissing"]["woodmissing"] > 1:

                        d["inv"].remove(item)
                        data["stash"]["stashmissing"]["woodmissing"] -= 1
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🪵 to the Stash creation. \n\nNow you only need "
                            + str(data["stash"]["stashmissing"]["woodmissing"])
                            + " "
                            + item
                            + " 🪵",
                        )
                    else:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " Your stash doesnt need "
                            + item
                            + " 🪵 for the next level.",
                        )
    elif len(message.text.split()) == 3:
        itemN = colN = message.text.split()[2]
        itemNu = int(itemN)
        if message.text.split()[1] == "stash":
            if stash.count(item) < itemNu:
                bot.send_message(message.chat.id, stashOnly)
            else:
                if data["stash"]["stashmissing"]["woodmissing"] < itemNu:
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " Your stash doesnt need that much "
                        + item
                        + " 🪵 for the next level.\n only missing: "
                        + str(data["stash"]["stashmissing"]["woodmissing"])
                        + " "
                        + item
                        + " 🪵",
                    )
                elif data["stash"]["stashmissing"]["woodmissing"] == itemNu:
                    key = "wood"

                    stashResources(d, data, message, name, itemNu, item, key)

                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + ", you  Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🪵 to the Stash creation using your Stash Supply.\n\nCongratz!! \n\nYou just finished gathering all the "
                        + item
                        + " 🪵 to build your Stash Lvl "
                        + str(data["stash"]["stashlevel"] + 1)
                        + "!\n\nChecking for a potential Lvl Up...",
                    )
                    stashLevelCheck(data, message, name)

                else:
                    key = "wood"
                    stashResources(d, data, message, name, itemNu, item, key)
                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " you Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🪵 to the Stash creation using your Stash supply. \n\nNow you only need "
                        + str(data["stash"]["stashmissing"]["stonemissing"])
                        + " "
                        + item
                        + " 🪵",
                    )

        else:
            if d["inv"].count(item) < itemNu:
                bot.send_message(message.chat.id, cOnly)
            else:
                if d["location"] != data['stash']['stashlocation']:
                    if d["gear"]["tele"] is False:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector is not at  "
                            + data['stash']['stashlocation']
                            + " and also hasn't a Teleportal  🔮 equipped!\n\nTo contribute to the Stash Creation  explore until you find "
                            + data['stash']['stashlocation']
                            + "!",
                        )
                    else:
                        if data["stash"]["stashmissing"]["woodmissing"] < itemNu:
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " Your stash doesnt need that much "
                                + item
                                + " 🪵 for the next level.\n only missing: "
                                + str(data["stash"]["stashmissing"]["woodmissing"])
                                + " "
                                + item
                                + " 🪵",
                            )
                        elif data["stash"]["stashmissing"]["woodmissing"] == itemNu:

                            cResources(d, data, message, name, itemNu, item, key)
                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🪵 to the Stash creation using his Teleportal 🔮. \n\nCongratz!! \n\nYou just finished gathering all the "
                                + item
                                + " 🪵 to build your Stash Lvl "
                                + str(data["stash"]["stashlevel"] + 1)
                                + "!\n\nChecking for a potential Lvl Up...",
                            )
                            stashLevelCheck(data, message, name)
                        else:

                            cResources(d, data, message, name, itemNu, item, key)
                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🪵 to the Stash creation using his Teleportal 🔮. \n\nNow you only need "
                                + str(data["stash"]["stashmissing"]["woodmissing"])
                                + " "
                                + item
                                + " 🪵",
                            )

                else:
                    if data["stash"]["stashmissing"]["woodmissing"] < itemNu:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " Your stash doesnt need that much "
                            + item
                            + " 🪵 for the next level.\n only missing: "
                            + str(data["stash"]["stashmissing"]["woodmissing"])
                            + " "
                            + item
                            + " 🪵",
                        )
                    elif data["stash"]["stashmissing"]["woodmissing"] == itemNu:
                        cResources(d, data, message, name, itemNu, item, key)
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🪵 to the Stash creation. \n\nCongratz!! \n\nYou just finished gathering all the "
                            + item
                            + " 🪵 to build your Stash Lvl "
                            + str(data["stash"]["stashlevel"] + 1)
                            + "!\n\nChecking for a potential Lvl Up...",
                        )
                        stashLevelCheck(data, message, name)
                    else:
                        cResources(d, data, message, name, itemNu, item, key)
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🪵 to the Stash creation. \n\nNow you only need "
                            + str(data["stash"]["stashmissing"]["woodmissing"])
                            + " "
                            + item
                            + " 🪵",
                        )
    else:
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + " you are doing something wrong. \n\nUse /stashwood <collector number> or simply:\n/stashwood for more info!",
        )


@bot.message_handler(commands=["stashstone", "ss"])
def stashstone(message):
    name = message.from_user.username
    item = "Granite Stone"
    key = "stone"
    data = load_from_userfile(name)
    colN = 1
    colNu = int(colN) - 1
    d = data["collectors"][colNu]
    stash = data["stash"]["stashinv"]
    data["stash"]["stashmissing"]["stonemissing"] = data["stash"]["stashmissing"][
        "stonemissing"
    ]
    itemNu = 1
    m1 = (
        "@"
        + name
        + " this command makes your collector contribute to the Stash development with "
        + str(itemNu)
        + " "
        + item
        + " 🪨from his inventory.\n\nPlease note that your collector needs to be at "
        + data['stash']['stashlocation']
        + " or Holding Teleportal 🔮 + 1 "
        + item
        + " 🪨 in inventory \n\n use  /stashstone <collector nr> or /stashstone <collector nr> <number> for bulk contribution. \nAlternatively you can contribute with items from your stash: \n /stashstone stash or stashstone stash <nr> for bulk contribution."
    )

    stashOnly = (
        "@"
        + name
        + ", Your Stash only has "
        + str(data["stash"]["stashinv"].count(item))
        + " "
        + item
        + "!\n\n🪨=❌"
    )
    cOnly = (
        "@"
        + name
        + ", Your Collector "
        + str(colN)
        + " only has "
        + str(d["inv"].count(item))
        + " "
        + item
        + "!\n\n🪨=❌"
    )

    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, m1)
    elif len(message.text.split()) == 2:
        if message.text.split()[1] == "stash":
            if item in stash:
                if data["stash"]["stashmissing"]["stonemissing"] == 1:

                    stash.remove(item)
                    data["stash"]["stashmissing"]["stonemissing"] -= 1
                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + ", you  Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🪨 to the Stash creation using your Stash Supply.\n\nCongratz!! \n\nYou just finished gathering all the "
                        + item
                        + " 🪨 to build your Stash Lvl "
                        + str(data["stash"]["stashlevel"] + 1)
                        + "!\n\nChecking for a potential Lvl Up...",
                    )
                    stashLevelCheck(data, message, name)
                elif data["stash"]["stashmissing"]["stonemissing"] > 1:

                    stash.remove(item)
                    data["stash"]["stashmissing"]["stonemissing"] -= 1
                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " you Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🪨 to the Stash creation using your Stash supply. \n\nNow you only need "
                        + str(data["stash"]["stashmissing"]["stonemissing"])
                        + " "
                        + item
                        + " 🪨",
                    )
                else:
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " Your stash doesnt need "
                        + item
                        + " 🪨 for the next level.",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    "@" + name + " Your stash doesnt hold any " + item + "!",
                )
        # from collector INV
        else:
            colN = message.text.split()[1]
            colNu = int(colN) - 1
            d = data["collectors"][colNu]
            if item not in d["inv"]:
                bot.send_message(
                    message.chat.id,
                    "@"
                    + name
                    + ", Your collector has no "
                    + item
                    + " on his inventory\n\n🪨=❌",
                )
            else:
                if d["location"] != data['stash']['stashlocation']:
                    if d["gear"]["tele"] is False:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector is not at  "
                            + data['stash']['stashlocation']
                            + " and also hasn't a Teleportal  🔮 equipped!\n\nTo contribute to the Stash Creation  explore until you find "
                            + data['stash']['stashlocation']
                            + "!",
                        )
                    else:
                        if data["stash"]["stashmissing"]["stonemissing"] == 1:

                            d["inv"].remove(item)
                            data["stash"]["stashmissing"]["stonemissing"] -= 1
                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🪨 to the Stash creation using his Teleportal 🔮. \n\nCongratz!! \n\nYou just finished gathering all the "
                                + item
                                + " 🪨 to build your Stash Lvl "
                                + str(data["stash"]["stashlevel"] + 1)
                                + "!\n\nChecking for a potential Lvl Up...",
                            )
                            stashLevelCheck(data, message, name)

                        elif data["stash"]["stashmissing"]["stonemissing"] > 1:

                            d["inv"].remove(item)
                            data["stash"]["stashmissing"]["stonemissing"] -= 1

                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🪨 to the Stash creation using his Teleportal 🔮. \n\nNow you only need "
                                + str(data["stash"]["stashmissing"]["stonemissing"])
                                + " "
                                + item
                                + " 🪨",
                            )
                        else:
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " Your stash doesnt need "
                                + item
                                + " 🪨 for the next level.",
                            )
                else:
                    if data["stash"]["stashmissing"]["stonemissing"] == 1:

                        d["inv"].remove(item)
                        data["stash"]["stashmissing"]["stonemissing"] -= 1
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🪨 to the Stash creation. \n\nCongratz!! \n\nYou just finished gathering all the "
                            + item
                            + " 🪨 to build your Stash Lvl "
                            + str(data["stash"]["stashlevel"] + 1)
                            + "!\n\nChecking for a potential Lvl Up...",
                        )
                        stashLevelCheck(data, message, name)

                    elif data["stash"]["stashmissing"]["stonemissing"] > 1:

                        d["inv"].remove(item)
                        data["stash"]["stashmissing"]["stonemissing"] -= 1
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🪨 to the Stash creation. \n\nNow you only need "
                            + str(data["stash"]["stashmissing"]["stonemissing"])
                            + " "
                            + item
                            + " 🪨",
                        )
                    else:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " Your stash doesnt need "
                            + item
                            + " 🪨 for the next level.",
                        )

    elif len(message.text.split()) == 3:
        itemN = colN = message.text.split()[2]
        itemNu = int(itemN)
        if message.text.split()[1] == "stash":
            if stash.count(item) < itemNu:
                bot.send_message(message.chat.id, stashOnly)
            else:
                if data["stash"]["stashmissing"]["stonemissing"] < itemNu:
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " Your stash doesnt need that much "
                        + item
                        + " 🪨 for the next level.\n only missing: "
                        + str(data["stash"]["stashmissing"]["stonemissing"])
                        + " "
                        + item
                        + " 🪨",
                    )
                elif data["stash"]["stashmissing"]["stonemissing"] == itemNu:
                    key = "stone"

                    stashResources(d, data, message, name, itemNu, item, key)
                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + ", you  Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🪨 to the Stash creation using your Stash Supply.\n\nCongratz!! \n\nYou just finished gathering all the "
                        + item
                        + " 🪨 to build your Stash Lvl "
                        + str(data["stash"]["stashlevel"] + 1)
                        + "!\n\nChecking for a potential Lvl Up...",
                    )
                    stashLevelCheck(data, message, name)

                else:
                    key = "stone"
                    stashResources(d, data, message, name, itemNu, item, key)
                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " you Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🪨 to the Stash creation using your Stash supply. \n\nNow you only need "
                        + str(data["stash"]["stashmissing"]["stonemissing"])
                        + " "
                        + item
                        + " 🪨",
                    )

        else:
            if d["inv"].count(item) < itemNu:
                bot.send_message(message.chat.id, cOnly)
            else:
                if d["location"] != data['stash']['stashlocation']:
                    if d["gear"]["tele"] is False:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector is not at  "
                            + data['stash']['stashlocation']
                            + " and also hasn't a Teleportal  🔮 equipped!\n\nTo contribute to the Stash Creation  explore until you find "
                            + data['stash']['stashlocation']
                            + "!",
                        )
                    else:
                        if data["stash"]["stashmissing"]["stonemissing"] < itemNu:
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " Your stash doesnt need that much "
                                + item
                                + " 🪨 for the next level.\n only missing: "
                                + str(data["stash"]["stashmissing"]["stonemissing"])
                                + " "
                                + item
                                + " 🪨",
                            )
                        elif (
                            data["stash"]["stashmissing"]["stonemissing"] == itemNu
                        ):

                            cResources(d, data, message, name, itemNu, item, key)
                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🪨 to the Stash creation using his Teleportal 🔮. \n\nCongratz!! \n\nYou just finished gathering all the "
                                + item
                                + " 🪨 to build your Stash Lvl "
                                + str(data["stash"]["stashlevel"] + 1)
                                + "!\n\nChecking for a potential Lvl Up...",
                            )
                            stashLevelCheck(data, message, name)
                        else:

                            cResources(d, data, message, name, itemNu, item, key)
                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🪨 to the Stash creation using his Teleportal 🔮. \n\nNow you only need "
                                + str(data["stash"]["stashmissing"]["stonemissing"])
                                + " "
                                + item
                                + " 🪨",
                            )

                else:
                    if data["stash"]["stashmissing"]["stonemissing"] < itemNu:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " Your stash doesnt need that much "
                            + item
                            + " 🪨 for the next level.\n only missing: "
                            + str(data["stash"]["stashmissing"]["stonemissing"])
                            + " "
                            + item
                            + " 🪨",
                        )
                    elif data["stash"]["stashmissing"]["stonemissing"] == itemNu:
                        cResources(d, data, message, name, itemNu, item, key)
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🪨 to the Stash creation. \n\nCongratz!! \n\nYou just finished gathering all the "
                            + item
                            + " 🪨 to build your Stash Lvl "
                            + str(data["stash"]["stashlevel"] + 1)
                            + "!\n\nChecking for a potential Lvl Up...",
                        )
                        stashLevelCheck(data, message, name)
                    else:
                        cResources(d, data, message, name, itemNu, item, key)
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🪨 to the Stash creation. \n\nNow you only need "
                            + str(data["stash"]["stashmissing"]["stonemissing"])
                            + " "
                            + item
                            + " 🪨",
                        )
    else:
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + " you are doing something wrong. \n\nUse /stashstone <collector number> or simply:\n/stashstone for more info!",
        )


@bot.message_handler(commands=["stashclay", "sc"])
def stashclay(message):
    name = message.from_user.username
    item = "Red Clay"
    key = "clay"
    data = load_from_userfile(name)
    colN = 1
    colNu = int(colN) - 1
    d = data["collectors"][colNu]
    stash = data["stash"]["stashinv"]
    data["stash"]["stashmissing"]["claymissing"] = data["stash"]["stashmissing"][
        "claymissing"
    ]
    itemNu = 1
    m1 = f"@{name}, this command makes your collector contribute to the Stash development with {itemNu} {item}" \
         f" 🧱from his inventory.\n\nPlease note that your collector needs to be at {data['stash']['stashlocation']} " \
         f"or Holding Teleportal 🔮 + 1 {item} 🧱 in inventory \n\n use  /stashclay <collector nr> or /stashclay " \
         f"<collector nr> <number> for bulk contribution. \nAlternatively you can contribute with items from your " \
         f"stash: \n /stashclay stash or stashclay stash <nr> for bulk contribution."

    stashOnly = (
        "@"
        + name
        + ", Your Stash only has "
        + str(data["stash"]["stashinv"].count(item))
        + " "
        + item
        + "!\n\n🧱=❌"
    )
    cOnly = (
        "@"
        + name
        + ", Your Collector "
        + str(colNu)
        + " only has "
        + str(d["inv"].count(item))
        + " "
        + item
        + "!\n\n🧱=❌"
    )

    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, m1)
    elif len(message.text.split()) == 2:
        if message.text.split()[1] == "stash":
            if item in stash:
                if data["stash"]["stashmissing"]["claymissing"] == 1:

                    stash.remove(item)
                    data["stash"]["stashmissing"]["claymissing"] -= 1
                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + ", you  Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🧱 to the Stash creation using your Stash Supply.\n\nCongratz!! \n\nYou just finished gathering all the "
                        + item
                        + " 🧱 to build your Stash Lvl "
                        + str(data["stash"]["stashlevel"] + 1)
                        + "!\n\nChecking for a potential Lvl Up...",
                    )
                    stashLevelCheck(data, message, name)
                elif data["stash"]["stashmissing"]["claymissing"] > 1:

                    stash.remove(item)
                    data["stash"]["stashmissing"]["claymissing"] -= 1
                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " you Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🧱 to the Stash creation using your Stash supply. \n\nNow you only need "
                        + str(data["stash"]["stashmissing"]["stonemissing"])
                        + " "
                        + item
                        + " 🧱",
                    )
                else:
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " Your stash doesnt need "
                        + item
                        + " 🧱 for the next level.",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    "@" + name + " Your stash doesnt hold any " + item + "!",
                )
        # from collector INV
        else:
            colN = message.text.split()[1]
            colNu = int(colN) - 1
            d = data["collectors"][colNu]
            if item not in d["inv"]:
                bot.send_message(
                    message.chat.id,
                    "@"
                    + name
                    + ", Your collector has no "
                    + item
                    + " on his inventory\n\n🧱=❌",
                )
            else:
                if d["location"] != data['stash']['stashlocation']:
                    if d["gear"]["tele"] is False:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector is not at  "
                            + data['stash']['stashlocation']
                            + " and also hasn't a Teleportal  🔮 equipped!\n\nTo contribute to the Stash Creation  explore until you find "
                            + data['stash']['stashlocation']
                            + "!",
                        )
                    else:
                        if data["stash"]["stashmissing"]["claymissing"] == 1:

                            d["inv"].remove(item)
                            data["stash"]["stashmissing"]["claymissing"] -= 1
                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🧱 to the Stash creation using his Teleportal 🔮. \n\nCongratz!! \n\nYou just finished gathering all the "
                                + item
                                + " 🧱 to build your Stash Lvl "
                                + str(data["stash"]["stashlevel"] + 1)
                                + "!\n\nChecking for a potential Lvl Up...",
                            )
                            stashLevelCheck(data, message, name)

                        elif data["stash"]["stashmissing"]["claymissing"] > 1:

                            d["inv"].remove(item)
                            data["stash"]["stashmissing"]["claymissing"] -= 1

                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🧱 to the Stash creation using his Teleportal 🔮. \n\nNow you only need "
                                + str(data["stash"]["stashmissing"]["claymissing"])
                                + " "
                                + item
                                + " 🧱",
                            )
                        else:
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " Your stash doesnt need "
                                + item
                                + " 🧱 for the next level.",
                            )
                else:
                    if data["stash"]["stashmissing"]["claymissing"] == 1:

                        d["inv"].remove(item)
                        data["stash"]["stashmissing"]["claymissing"] -= 1
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🧱 to the Stash creation. \n\nCongratz!! \n\nYou just finished gathering all the "
                            + item
                            + " 🧱 to build your Stash Lvl "
                            + str(data["stash"]["stashlevel"] + 1)
                            + "!\n\nChecking for a potential Lvl Up...",
                        )
                        stashLevelCheck(data, message, name)

                    elif data["stash"]["stashmissing"]["claymissing"] > 1:

                        d["inv"].remove(item)
                        data["stash"]["stashmissing"]["claymissing"] -= 1
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🧱 to the Stash creation. \n\nNow you only need "
                            + str(data["stash"]["stashmissing"]["claymissing"])
                            + " "
                            + item
                            + " 🧱",
                        )
                    else:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " Your stash doesnt need "
                            + item
                            + " 🧱 for the next level.",
                        )

    elif len(message.text.split()) == 3:
        itemN = colN = message.text.split()[2]
        itemNu = int(itemN)
        if message.text.split()[1] == "stash":
            if stash.count(item) < itemNu:
                bot.send_message(message.chat.id, stashOnly)
            else:
                if data["stash"]["stashmissing"]["claymissing"] < itemNu:
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " Your stash doesnt need that much "
                        + item
                        + " 🧱 for the next level.\n only missing: "
                        + str(data["stash"]["stashmissing"]["claymissing"])
                        + " "
                        + item
                        + " 🧱",
                    )
                elif data["stash"]["stashmissing"]["claymissing"] == itemNu:
                    key = "clay"

                    stashResources(d, data, message, name, itemNu, item, key)
                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + ", you  Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🧱 to the Stash creation using your Stash Supply.\n\nCongratz!! \n\nYou just finished gathering all the "
                        + item
                        + " 🧱 to build your Stash Lvl "
                        + str(data["stash"]["stashlevel"] + 1)
                        + "!\n\nChecking for a potential Lvl Up...",
                    )
                    stashLevelCheck(data, message, name)

                else:
                    key = "clay"
                    stashResources(d, data, message, name, itemNu, item, key)
                    save_to_userfile(data, name)
                    bot.send_message(
                        message.chat.id,
                        "@"
                        + name
                        + " you Sucessfuly contributed with "
                        + str(itemNu)
                        + " "
                        + item
                        + " 🪨 to the Stash creation using your Stash supply. \n\nNow you only need "
                        + str(data["stash"]["stashmissing"]["claymissing"])
                        + " "
                        + item
                        + " 🪨",
                    )

        else:
            if d["inv"].count(item) < itemNu:
                bot.send_message(message.chat.id, cOnly)
            else:
                if d["location"] != data['stash']['stashlocation']:
                    if d["gear"]["tele"] is False:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector is not at  "
                            + data['stash']['stashlocation']
                            + " and also hasn't a Teleportal  🔮 equipped!\n\nTo contribute to the Stash Creation  explore until you find "
                            + data['stash']['stashlocation']
                            + "!",
                        )
                    else:
                        if data["stash"]["stashmissing"]["claymissing"] < itemNu:
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " Your stash doesnt need that much "
                                + item
                                + " 🧱 for the next level.\n only missing: "
                                + str(data["stash"]["stashmissing"]["claymissing"])
                                + " "
                                + item
                                + " 🧱",
                            )
                        elif data["stash"]["stashmissing"]["claymissing"] == itemNu:

                            cResources(d, data, message, name, itemNu, item, key)
                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🧱 to the Stash creation using his Teleportal 🔮. \n\nCongratz!! \n\nYou just finished gathering all the "
                                + item
                                + " 🧱 to build your Stash Lvl "
                                + str(data["stash"]["stashlevel"] + 1)
                                + "!\n\nChecking for a potential Lvl Up...",
                            )
                            stashLevelCheck(data, message, name)
                        else:

                            cResources(d, data, message, name, itemNu, item, key)
                            save_to_userfile(data, name)
                            bot.send_message(
                                message.chat.id,
                                "@"
                                + name
                                + " your Collector Sucessfuly contributed with "
                                + str(itemNu)
                                + " "
                                + item
                                + " 🧱 to the Stash creation using his Teleportal 🔮. \n\nNow you only need "
                                + str(
                                    data["stash"]["stashmissing"]["claymissing"]
                                    - itemNu
                                )
                                + " "
                                + item
                                + " 🧱",
                            )

                else:
                    if data["stash"]["stashmissing"]["claymissing"] < itemNu:
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " Your stash doesnt need that much "
                            + item
                            + " 🧱 for the next level.\n only missing: "
                            + str(data["stash"]["stashmissing"]["claymissing"])
                            + " "
                            + item
                            + " 🧱",
                        )
                    elif data["stash"]["stashmissing"]["claymissing"] == itemNu:
                        cResources(d, data, message, name, itemNu, item, key)
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🧱 to the Stash creation. \n\nCongratz!! \n\nYou just finished gathering all the "
                            + item
                            + " 🧱 to build your Stash Lvl "
                            + str(data["stash"]["stashlevel"] + 1)
                            + "!\n\nChecking for a potential Lvl Up...",
                        )
                        stashLevelCheck(data, message, name)
                    else:
                        cResources(d, data, message, name, itemNu, item, key)
                        save_to_userfile(data, name)
                        bot.send_message(
                            message.chat.id,
                            "@"
                            + name
                            + " your Collector Sucessfuly contributed with "
                            + str(itemNu)
                            + " "
                            + item
                            + " 🧱 to the Stash creation. \n\nNow you only need "
                            + str(
                                data["stash"]["stashmissing"]["claymissing"]
                                - itemNu
                            )
                            + " "
                            + item
                            + " 🧱",
                        )
    else:
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + " you are doing something wrong. \n\nUse /stashclay <collector number> or simply:\n/stashclay for more info!",
        )


@bot.message_handler(commands=["eat"])
def bot_eat(message):
    fruit = ["Friendship Cookie", "Orange", "Fig", "Barbary Fig", "Wild Berries"]
    name = message.from_user.username
    data = load_from_userfile(name)
    if len(message.text.split()) == 1:
        bot.send_message(
            message.chat.id,
            "🍽 *EAT* 🍽 \n\n *Eat allows your collector to consume a piece of food he holds in his inventory, replenishing his Calorie Count.* \n\nTo eat, *use the command* /eat <Collector nr> <item nr>\nReplace <Collector nr> with the number of the collector you want to perform the action with.\nReplace <item nr> with the index nr of the item you want to eat.\n\nIn case of doubt use /inv or /inv <Collector nr> To find more info.\n\n End of report 🧐",
            parse_mode="Markdown",
        )
    elif len(message.text.split()) == 3:
        colN = message.text.split()[1]
        colNu = int(colN) - 1
        d = data["collectors"][colNu]
        itemN = int(message.text.split()[2]) - 1
        item = d["inv"][itemN]
        if d["inv"][itemN] in fruit:
            print("ok")
            eat(d, data, item, message, name)
        else:
            bot.send_message(
                message.chat.id,
                "*@"
                + name
                + ", Your collector can't eat "
                + str(d["inv"][itemN])
                + "! \n\n But good try anyway.*",
                parse_mode="Markdown",
            )
    elif len(message.text.split()) == 2:
        colN = message.text.split()[1]
        colNu = int(colN) - 1
        d = data["collectors"][colNu]
        bot.send_message(
            message.chat.id,
            "🍽 *EAT* 🍽 \n\n @"
            + name
            + " *you successfully selected collector* "
            + str(colN)
            + ", *yet you havent selected any item from his inventory to be consumed*. \n to help you out, below you have a list of the items on his inventory.\n\n *INVENTORY Collector:* "
            + str(colN)
            + "\n\n "
            + str(d["inv"])
            + "\n\n*Items are numbered by the order they are shown. if you want to eat item 1 from Collector* "
            + str(colN)
            + "*simply type: /eat "
            + str(colN)
            + " 1, and so on, so on..\n\n End of report 🧐*",
            parse_mode="Markdown",
        )

    else:
        print("shit")


@bot.message_handler(commands=["stash"])
def stash(message):
    name = message.from_user.username
    data = load_from_userfile(name)
    m = (
        "📦*STASH*📦\n\n*The Stash is where you will eventually build your Hut and will work as a secondary base*.\n\n You are able to *store your findings on the Stash*, and from it you *unlock the capacity to craft* in game items that *can be redeemed as NFTs*.\n\n*To interact with the Stash, the Collector needs to be on the same Terrain as the personal Stash is located.*\n\n *STASH INFO*\n\n*Stash Lvl:* "
        + str(data["stash"]["stashlevel"])
        + "\n*Stash Location:* "
        + str(data['stash']['stashlocation'])
        + "\n🪵 *Wood Missing:* "
        + str(data["stash"]["stashmissing"]["woodmissing"])
        + "\n🪨 *Granite Missing:* "
        + str(data["stash"]["stashmissing"]["stonemissing"])
        + "\n🧱 *Clay Missing:* "
        + str(data["stash"]["stashmissing"]["claymissing"])
        + "\n *Nail Missing:* "
        + str(data["stash"]["stashmissing"]["nailmissing"])
        + "\n\n🌌 *Current Available Space:* "
        + str(data["stash"]["stashspace"] - int(len(data["stash"]["stashinv"])))
        + "\n📦 *Current Stash Inventory:* "
        + str(data["stash"]["stashinv"])
        + "\n\n *End of report 🧐*"
    )

    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, m, parse_mode="Markdown")
    elif len(message.text.split()) == 2:
        bot.send_message(message.chat.id, m, parse_mode="Markdown")
    elif len(message.text.split()) == 3:
        colN = message.text.split()[1]
        colNu = int(colN) - 1
        item = message.text.split()[2]
        itemNu = int(item) - 1
        d = data["collectors"][colNu]
        stashInvCount = len(data["stash"]["stashinv"])
        if d["gear"]["tele"] and data["stash"]["stashlevel"] > 0:

            n = (
                " 📦*STASH*📦\n\n *Your Collector* "
                + str(colN)
                + " *can't send any items because your Stash is Full. *❌"
            )
            o = (
                " 📦*STASH*📦\n\n* Your Collector* "
                + str(colN)
                + " *successfully sent over* "
                + str(d["inv"][itemNu])
                + "* to your Stash, using Teleportal *🔮! ✅\n\n*Stash Available Space:* "
                + str(data["stash"]["stashspace"] - stashInvCount - 1)
            )
            if stashInvCount >= data["stash"]["stashspace"]:
                print("no space")
                bot.send_message(message.chat.id, n, parse_mode="Markdown")
            else:
                data["stash"]["stashinv"].append(d["inv"][itemNu])
                del d["inv"][itemNu]
                stashInvCount = len(data["stash"]["stashinv"])
                save_to_userfile(data, name)
                bot.send_message(message.chat.id, o, parse_mode="Markdown")
                # non tp holders
        elif (
            d["location"] == data['stash']['stashlocation']
            and data["stash"]["stashlevel"] > 0
        ):
            n = (
                " 📦*STASH*📦\n\n *Your Collector* "
                + str(colN)
                + " *can't send any items because your Stash is Full. *❌"
            )
            o = (
                " 📦*STASH*📦\n\n *Your Collector* "
                + str(colN)
                + " *successfully sent over* "
                + str(d["inv"][itemNu])
                + " *to your Stash!*  ✅\n\n*Stash Available Space:* "
                + str(data["stash"]["stashspace"] - stashInvCount)
                + "\n\n*Stash Inventory:*\n"
                + str(data["stash"]["stashinv"])
            )
            if stashInvCount >= data["stash"]["stashspace"]:
                bot.send_message(message.chat.id, n, parse_mode="Markdown")
            else:
                data["stash"]["stashinv"].append(d["inv"][itemNu])
                item = d["inv"][itemNu]
                del d["inv"][itemNu]
                stashInvCount = len(data["stash"]["stashinv"])
                save_to_userfile(data, name)
                o = (
                    " 📦*STASH*📦\n\n *Your Collector* "
                    + str(colN)
                    + " *successfully sent over* "
                    + str(item)
                    + " *to your Stash!*  ✅\n\n*Stash Available Space:* "
                    + str(data["stash"]["stashspace"] - stashInvCount)
                    + "\n\n*Stash Inventory:*\n"
                    + str(data["stash"]["stashinv"])
                )
                bot.send_message(message.chat.id, o, parse_mode="Markdown")


@bot.message_handler(commands=["market"])
def market(message):
    if len(message.text.split()) == 1:
        bot.send_message(
            message.chat.id,
            f"⚖ *MARKET* ⚖\n\n"
            f"The Market allows you to *make commerce inside the game*.\n\n"
            f"If you hold a *Collectors License* and a *Stash*. you can use the Market *without limitations*. "
            f"If you dont hold a Collector License, then you *can only buy from the Market*⚖ \nThe prices are "
            f"fixed and the supply is limited. \n*PRICE RATES*!\n\n*Price Table*\n\n🍐 *Food* 🍪\n\n1 *Friendship "
            f"Cookie* 🍪 = 1 Coin \n/buycookie or /sellcookie\n*Wild Berries* 🫐 = 1 Coin\n/buyberries or "
            f"/sellberries\n1 *Fig* 🍐 = 1 Coin\n/buyfig or /sellfig\n1 *Orange* 🍊 = 1 Coin\n/buyorange or "
            f"/sellorange \n1 *Barbary Fig* 🌵🍐 = 1 Coin\n/buybfig or /sellbfig\n\n🪨*RAW MATERIALS*🪵\n"
            f"2 *Seed* 🌱 = 1 Coin\n/buyseed or /sellseed\n1 *Grass Tuft* 🌿 = 1 Coin\n/buygrass or /sellgrass\n"
            f"2 *Dried Leaf* 🍁 = 1 Coin\n/buydleaf or /selldleaf\n2 *Excrement* 💩 = 1 Coin\n/buyexcrement or "
            f"/sellexcrement\n2 *Rag* 📜 = 1 Coin\n/buyrag or /sellrag\n2 *Small Bone* 🦴 = 1 Coin\n/buysbone or "
            f"/sellsbone\n1 *Wood* 🪵 = 1 Coin\n/buywood or /sellwood\n1 *Pinecone* 🌲 = 1 Coin\n/buypinecone or "
            f"/sellpinecone\n1 *Tree Bark* 🌳 = 1 Coin\n/buytbark or /selltbark\n1 *Green Mushroom* 🟢🍄 = 1 Coin\n"
            f"/buygmushroom or /sellgmushroom\n1 *Whitestone* ⚪️🪨 = 1 Coin\n/buywhitestone or /sellwhitestone\n"
            f"1 *Granite Stone* 🪨 = 1 Coin\n/buygranite or /sellgranite\n1 *Seagull Egg* 🥚 = 1 Coin\n/buysegg or "
            f"/sellsegg\n 1 *Gravel*  = 1 Coin\n/buygravel or /sellgravel\n1 *Whetstone* 💧🪨 = 2 Coins\n/buywhetstone "
            f"or /sellwhetstone\n1 *Big Flat Stone* 🪨 = 2 Coins\n/buybfstone or /sellbfstone\n"
            f"1 *Drift Wood* 💧🪵 = 1 Coin\n/buydwood or /selldwood\n1 *Shell* 🐚 = 1 Coin\n/buyshell or /sellshell\n"
            f"1 *Flat Stone* 🪨 = 1 Coin\n/buyfstone or /sellfstone\n1 *Clam* 🐚 = 1 Coin\n/buyclam or /sellclam\n"
            f"2 *Salty Water* = 1 Coin\n/buyswater or /sellswater\n2 *Water* 💧 = 1 Coin\n/buywater or /sellwater\n"
            f"1 *Rusty Nail* = 1 Coin\n/buyrnail or /sellrnail\n1 *Rusty Needle* 🪡 = 2 Coins\n/buyrneedle or "
            f"/sellrneedle\n1 *Rusty Spike* = 3 Coins\n/buyrspike or /sellrspike\n1 *Resin* 🟡💧 = 2 Coins\n"
            f"/buyresin or /sellresin\n1 *Bamboo* 🎋 = 1 Coin\n/buybamboo or /sellbamboo\n\n🖐 *MANUFACTURED* ⚒\n\n"
            f"Coming Soon...\n\n*To Check Market Supply use commands below:\n\n/foodsupply\n/rawsupply*",
            parse_mode="Markdown",
        )


@bot.message_handler(commands=["foodsupply", "fs"])
def foodsupply(message):
    if len(message.text.split()) == 1:
        data = load_from_market()
        food_data = data["food"]
        info = json.dumps(food_data, indent=4)
        bot.send_message(message.chat.id, "🥙  Food Market Supply 🛒\n\n" + info)


@bot.message_handler(commands=["rawsupply", "rs"])
def rawsupply(message):
    if len(message.text.split()) == 1:
        data = load_from_market()
        food_data = data["rawmaterials"]
        info = json.dumps(food_data, indent=4)
        bot.send_message(
            message.chat.id, "🪨 Raw Materials Market Supply 🛒\n\n" + info
        )


@bot.message_handler(commands=["coinsupply", "cs"])
def coinsupply(message):
    if len(message.text.split()) == 1:
        data = load_from_market()
        food_data = data["coins"]
        info = json.dumps(food_data, indent=4)
        bot.send_message(message.chat.id, "💰 Coin Market Supply 💰\n\n" + info)


@bot.message_handler(commands=["buyfood", "bf"])
def buyfood(message):
    name = message.from_user.username
    n = "🥙  Food Market Index 🛒\n\n 1. Friendship Cookie\n2. Wild Berries\n3. Barbary Fig\n 4. Orange\n5. Fig"
    m = (
        "            BUY FOOD\n\nWith this command you can use your earned Coins to buy Food to consume in game or withdraw. \n\n             To buy anything use the the command:\n        /buyfood <collector nr> <item number> \n ✅ Replace <collector nr> with the number of the collector that will receive the item on his inventory\n ✅ Replace <item name> with the item nr of the item you want to buy\n\n"
        + n
        + "\n\n⚠ It is advisable that you check market supply before trying to buy anything! ⚠ \nTo do so use the command /foodsupply"
    )
    o = (
        " ⚠ The number you provide as index doesnt brought any result. ⚠\n\nPlease check the Food Market Index:\n\n"
        + n
    )
    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, m)
    elif len(message.text.split()) == 2:
        bot.send_message(message.chat.id, m)
    if len(message.text.split()) == 3:
        data = load_from_userfile(name)
        colN = message.text.split()[1]
        colNu = int(colN) - 1
        d = data["collectors"][colNu]
        item = message.text.split()[2]
        itemN = int(item) - 1
        list = (0, 4)
        if itemN not in list:
            bot.send_message(message.chat.id, o)
        elif itemN in list:
            if data["ccoins"] > 0:
                name = message.from_user.username
                print(name)
                checkFoodSupply(d, data, name, message, itemN)
            else:
                bot.send_message(
                    message.chat.id,
                    "@"
                    + name
                    + ", you dont have Coins to purchase this item!\n\nYou have: "
                    + str(data["ccoins"])
                    + " Coins!\n\nTry again when you earn some!",
                )


@bot.message_handler(commands=["buyrnail"])
def buyrnail(message):
    name = message.from_user.username
    cost = 1
    space = 1
    minimum = 1
    type = "rawmaterials"
    item = "Rusty Nail"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= minimum:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellrnail"])
def sellrnail(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Rusty Nail"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min
                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellshell"])
def sellshell(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Shell"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + " for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyclam"])
def buyclam(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Clam"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellclam"])
def sellclam(message):
    name = message.from_user.username
    cost = 1
    space = 1
    minimum = 1
    type = "rawmaterials"
    item = "Clam"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= minimum:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += minimum

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(minimum)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(minimum)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(minimum)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buycookie"])
def buycookie(message):
    name = message.from_user.username
    cost = 1
    space = 1
    minimum = 1
    type = "food"
    item = "Friendship Cookie"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= minimum:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellcookie"])
def sellcookie(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "food"
    item = "Friendship Cookie"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData["food"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + " for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyresin"])
def buyresin(message):
    name = message.from_user.username
    cost = 2
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Resin"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellresin"])
def sellresin(message):
    name = message.from_user.username
    cost = 2
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Resin"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyrspike"])
def buyrspike(message):
    name = message.from_user.username
    cost = 3
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Rusty Spike"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellrspike"])
def sellrspike(message):
    name = message.from_user.username
    cost = 3
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Rusty Spike"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyseed"])
def buyseed(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Seed"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellseed"])
def sellseed(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Seed"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            data["stash"]["stashinv"].remove(item)
                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buydleaf"])
def buydleaf(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Dried Leaf"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["selldleaf"])
def selldleaf(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Dried Leaf"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            data["stash"]["stashinv"].remove(item)
                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + " for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyexcrement"])
def buyexcrement(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Excrement"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellexcrement"])
def sellexcrement(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Excrement"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            data["stash"]["stashinv"].remove(item)
                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + " for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyrag"])
def buyrag(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Rag"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellrag"])
def sellrag(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Rag"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            data["stash"]["stashinv"].remove(item)
                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buysbone"])
def buysbone(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Small Bone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellsbone"])
def sellsbone(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Small Bone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            data["stash"]["stashinv"].remove(item)
                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector Licens�e✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buywhetstone"])
def buywhetstone(message):
    name = message.from_user.username
    cost = 2
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Whetstone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellwhetstone"])
def sellwhetstone(message):
    name = message.from_user.username
    cost = 2
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Whetstone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)

                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buybfstone"])
def buybfstone(message):
    name = message.from_user.username
    cost = 2
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Big Flat Stone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED� ❌🛒",
                )


@bot.message_handler(commands=["sellbfstone"])
def sellbfstone(message):
    name = message.from_user.username
    cost = 2
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Big Flat Stone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)

                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buywater"])
def buywater(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Water"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellwater"])
def sellwater(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Water"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            data["stash"]["stashinv"].remove(item)

                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyswater"])
def buyswater(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Salty Water"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellswater"])
def sellswater(message):
    name = message.from_user.username
    cost = 1
    space = 2
    min = 2
    type = "rawmaterials"
    item = "Salty Water"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            data["stash"]["stashinv"].remove(item)

                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyrneedle"])
def buyrneedle(message):
    name = message.from_user.username
    cost = 2
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Rusty Needle"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= min
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellrneedle"])
def sellrneedle(message):
    name = message.from_user.username
    cost = 2
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Rusty Needle"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + str(min)
                                + " "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellberries"])
def sellberries(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "food"
    item = "Wild Berries"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData["food"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyberries"])
def buyberries(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "food"
    item = "Wild Berries"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMar�ket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellbfig"])
def sellbfig(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "food"
    item = "Barbary Fig"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData["food"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buybfig"])
def buybfig(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "food"
    item = "Barbary Fig"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellfig"])
def sellfig(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "food"
    item = "Fig"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData["food"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyfig"])
def buyfig(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "food"
    item = "Fig"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellorange"])
def sellorange(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "food"
    item = "Orange"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData["food"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyorange"])
def buyorange(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "food"
    item = "Orange"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


# Raw


@bot.message_handler(commands=["sellwood"])
def sellwood(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Plain Wood"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData["rawmaterials"][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅ \n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + " for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector L�icense ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buywood"])
def buywood(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Plain Wood"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


# GrASS


@bot.message_handler(commands=["buygrass"])
def buygrass(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Grass Tuft"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellgrass"])
def sellgrass(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Plain Wood"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buypinecone"])
def buypinecone(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Pinecone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellpinecone"])
def sellpinecone(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Pinecone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buytbark"])
def buytbark(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Tree Bark"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["selltbark"])
def selltbark(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Tree Bark"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buygmushroom"])
def buygmushroom(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Green Mushroom"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellgmushroom"])
def sellgmushroom(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Green Mushroom"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buywhitestone"])
def buywhitestone(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Whitestone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellwhitestone"])
def sellwhitestone(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Whitestone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + "for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buygranite"])
def buygranite(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Granite Stone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellgranite"])
def sellgranite(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Granite Stone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + " for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buysegg"])
def buysegg(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Seagull Egg"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellsegg"])
def sellsegg(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Seagull Egg"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + " for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buygravel"])
def buygravel(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Gravel"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "\nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellgravel"])
def sellgravel(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Gravel"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + " for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buydwood"])
def buydwood(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Drift Wood"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "\n\nStash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["selldwood"])
def selldwood(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Drift Wood"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + " for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyshell"])
def buyshell(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Shell"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] >= min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!nStash 📦 Available ✅\n ❌ @"
                        + name
                        + "n\n\Stash 📦 Space: "
                        + str(tspace)
                        + "nMarket Supply: "
                        + item
                        + "="
                        + str(marketData[type][item]["count"])
                        + "❌ nn 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["buyfstone"])
def buyfstone(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Flat Stone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            if data["stash"]["stashlevel"] > 0:
                tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
                if tspace >= space and marketData[type][item]["count"] > min:
                    if data["ccoins"] >= cost:
                        data["ccoins"] -= cost
                        data["stash"]["stashinv"].append(item)
                        marketData["coins"] += cost
                        marketData[type][item]["count"] -= 1
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nand user has enough coins✅\n@"
                            + name
                            + ", you bought "
                            + item
                            + " for "
                            + str(cost)
                            + "\n\n 🛒✅ PURCHASE SUCCESSFUL  ✅🛒",
                        )
                        save_to_userfile(data, name)
                        save_to_market(marketData)
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 BUYING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅\nStash 📦 has available Space ✅\nMarket has enough supply: "
                            + item
                            + "✅\nBut @"
                            + name
                            + " has not enough coins ❌ \n\n 🛒❌ PURCHASE FAILED  ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 BUYING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅\n ❌ @"
                        + name
                        + ", you dont have enough space in your Stash 📦 to finish this trade ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 BUYING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ PURCHASE FAILED ❌🛒",
                )


@bot.message_handler(commands=["sellfstone"])
def sellfstone(message):
    name = message.from_user.username
    cost = 1
    space = 1
    min = 1
    type = "rawmaterials"
    item = "Flat Stone"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["collectorlicense"]:
                    if data["stash"]["stashinv"].count(item) >= min:
                        if marketData["coins"] >= cost:
                            marketData["coins"] -= cost
                            data["stash"]["stashinv"].remove(item)
                            marketData[type][item]["count"] += min

                            data["ccoins"] += cost
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has enough Coins ✅\n@"
                                + name
                                + ", you sold "
                                + item
                                + " for "
                                + str(cost)
                                + "\n\n 🛒✅ SALE SUCCESSFUL  ✅🛒",
                            )
                            save_to_userfile(data, name)
                            print("saved")
                            save_to_market(marketData)
                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛒 SELLING 🛒"
                                + item
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has Collector License✅ \nStash 📦 has "
                                + str(min)
                                + " "
                                + item
                                + "! ✅\nMarket has NOT enough Coins. ❌\n@"
                                + name
                                + " try again another time. ❌ \n\n 🛒❌ SALE FAILED  ❌🛒",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛒 SELLING 🛒"
                            + item
                            + "!!\n Stash 📦 Available ✅@"
                            + name
                            + " has Collector License✅ \n Stash 📦 does not have "
                            + str(min)
                            + " "
                            + item
                            + "❌ @"
                            + name
                            + ", try again when you hold to finish this trade ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛒 SELLING 🛒"
                        + item
                        + "!!\n Stash 📦 Available ✅@"
                        + name
                        + " don't have' Collector License ❌ \n@"
                        + name
                        + ", try again when you have the License ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛒 SELLING 🛒"
                    + item
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, so this trade is cancelled ❌ \n\n 🛒❌ SALE FAILED ❌🛒",
                )


@bot.message_handler(commands=["craftrope"])
def craftrope(message):
    name = message.from_user.username
    cost = 3
    ingredient = "Grass Tuft"
    type = "rawmaterials"
    output = "Weak Rope"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].append(output)
                    # data["craftC"] += 1
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + "! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again once you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )


@bot.message_handler(commands=["craftfireplace"])
def craftfireplace(message):
    name = message.from_user.username
    cost = 8
    ingredient = "Granite Stone"
    type = "rawmaterials"
    output = "Fire Place"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    # data["craftC"] += 1
                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + "! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again once you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )


@bot.message_handler(commands=["craftfence"])
def craftfence(message):
    name = message.from_user.username
    cost = 4
    ingredient = "Plain Wood"
    type = "rawmaterials"
    output = "Wood Fence"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + "! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again when you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )


@bot.message_handler(commands=["craftpellet"])
def craftpellet(message):
    name = message.from_user.username
    cost = 1
    ingredient = "Excrement"
    type = "rawmaterials"
    output = "Excrement Pellet"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)

                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + "! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again when you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )


@bot.message_handler(commands=["crafttbchips"])
def crafttbchips(message):
    name = message.from_user.username
    cost = 2
    ingredient = "Tree Bark"
    type = "rawmaterials"
    output = "Tree Bark Chips"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)

                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + "! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved " + name)
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again when you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )


@bot.message_handler(commands=["craftcompost"])
def craftcompost(message):
    name = message.from_user.username
    ingredient = "Excrement"
    cost = 1
    ingredient2 = "Dried Leaf"
    cost2 = 2
    type = "rawmaterials"
    output = "Compost 1"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if (
                    data["stash"]["stashinv"].count(ingredient) >= cost
                    and data["stash"]["stashinv"].count(ingredient2) >= cost2
                ):
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient2)
                    data["stash"]["stashinv"].remove(ingredient2)
                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + "\n And "
                        + str(cost2)
                        + " "
                        + ingredient2
                        + "! ✅\nYou successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + "\nand "
                        + str(data["stash"]["stashinv"].count(ingredient2))
                        + " "
                        + ingredient2
                        + "❌\nTry again when you have the required ingredients! ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )


@bot.message_handler(commands=["craftbonehook"])
def craftbonehook(message):
    name = message.from_user.username
    cost = 1
    ingredient = "Small Bone"
    type = "rawmaterials"
    output = "Bone Hook"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        if data["stash"]["tools"]["knife"]:
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + " and also has Handy Knife 🔪! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again when you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has no Handy Knife 🔪❌\n\n 🛠❌ CRAFT FAILED  ❌🛠",
                )
        else:
            bot.send_message(
                message.chat.id,
                " 🛠 CRAFTING 🛠"
                + output
                + "!!\n Stash 📦 Not Available ❌\n  @"
                + name
                + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
            )


@bot.message_handler(commands=["craftwoodframe"])
def craftwoodframe(message):
    name = message.from_user.username
    cost = 5
    ingredient = "Plain Wood"
    type = "rawmaterials"
    output = "Wood Frame"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        if data["stash"]["tools"]["knife"]:
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)

                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + " and also has Handy Knife 🔪! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again when you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has no Handy Knife 🔪❌\n\n 🛠❌ CRAFT FAILED  ❌🛠",
                )
        else:
            bot.send_message(
                message.chat.id,
                " 🛠 CRAFTING 🛠"
                + output
                + "!!\n Stash 📦 Not Available ❌\n  @"
                + name
                + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
            )


@bot.message_handler(commands=["craftweakbow"])
def craftweakbow(message):
    name = message.from_user.username
    ingredient = "Plain Wood"
    cost = 2
    ingredient2 = "Weak Rope"
    cost2 = 2
    type = "rawmaterials"
    output = "Weak Bow"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if (
                    data["stash"]["stashinv"].count(ingredient) >= cost
                    and data["stash"]["stashinv"].count(ingredient2) >= cost2
                ):
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient2)
                    data["stash"]["stashinv"].remove(ingredient2)
                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + "\n And "
                        + str(cost2)
                        + " "
                        + ingredient2
                        + "! ✅\nYou successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + "\nand "
                        + str(data["stash"]["stashinv"].count(ingredient2))
                        + " "
                        + ingredient2
                        + "❌\nTry again when you have the required ingredients! ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )


@bot.message_handler(commands=["craftfishingrod"])
def craftfishingrod(message):
    name = message.from_user.username
    ingredient = "Plain Wood"
    cost = 2
    ingredient2 = "Weak Rope"
    cost2 = 1
    ingredient3 = "Bone Hook"
    cost3 = 1
    type = "rawmaterials"
    output = "Weak Fishing Rod"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    if data["stash"]["stashinv"].count(ingredient2) >= cost2:
                        if data["stash"]["stashinv"].count(ingredient3) >= cost3:
                            data["stash"]["stashinv"].remove(ingredient)
                            data["stash"]["stashinv"].remove(ingredient)
                            data["stash"]["stashinv"].remove(ingredient2)
                            data["stash"]["stashinv"].remove(ingredient3)
                            data["stash"]["stashinv"].append(output)
                            bot.send_message(
                                message.chat.id,
                                " 🛠 CRAFTING 🛠"
                                + output
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has "
                                + str(cost)
                                + " "
                                + ingredient
                                + "\n "
                                + str(cost2)
                                + " "
                                + ingredient2
                                + "\nand "
                                + str(cost3)
                                + " "
                                + ingredient3
                                + "! ✅\nYou successfully crafted "
                                + output
                                + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                            )
                            save_to_userfile(data, name)
                            print("saved")

                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛠 CRAFTING 🛠"
                                + output
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has "
                                + str(data["stash"]["stashinv"].count(ingredient))
                                + " "
                                + ingredient
                                + "\n "
                                + str(data["stash"]["stashinv"].count(ingredient2))
                                + " "
                                + ingredient2
                                + "\n And "
                                + str(data["stash"]["stashinv"].count(ingredient3))
                                + " "
                                + ingredient3
                                + " ❌\nTry again when you have the required ingredients! ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛠 CRAFTING 🛠"
                            + output
                            + "!!\n Stash 📦 Available ✅\n@"
                            + name
                            + " has "
                            + str(data["stash"]["stashinv"].count(ingredient))
                            + " "
                            + ingredient
                            + "\n "
                            + str(data["stash"]["stashinv"].count(ingredient2))
                            + " "
                            + ingredient2
                            + "\n And "
                            + str(data["stash"]["stashinv"].count(ingredient3))
                            + " "
                            + ingredient3
                            + " ❌\nTry again when you have the required ingredients! ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + "\n "
                        + str(data["stash"]["stashinv"].count(ingredient2))
                        + " "
                        + ingredient2
                        + "\n And "
                        + str(data["stash"]["stashinv"].count(ingredient3))
                        + " "
                        + ingredient3
                        + " ❌\nTry again when you have the required ingredients! ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )


@bot.message_handler(commands=["craftstoneaxe"])
def craftstoneaxe(message):
    name = message.from_user.username
    ingredient = "Plain Wood"
    cost = 2
    ingredient2 = "Weak Rope"
    cost2 = 1
    ingredient3 = "Flat Stone"
    cost3 = 1
    type = "rawmaterials"
    output = "Stone Axe"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    if data["stash"]["stashinv"].count(ingredient2) >= cost2:
                        if data["stash"]["stashinv"].count(ingredient3) >= cost3:
                            data["stash"]["stashinv"].remove(ingredient)
                            data["stash"]["stashinv"].remove(ingredient)
                            data["stash"]["stashinv"].remove(ingredient2)
                            data["stash"]["stashinv"].remove(ingredient3)
                            data["stash"]["stashinv"].append(output)
                            bot.send_message(
                                message.chat.id,
                                " 🛠 CRAFTING 🛠"
                                + output
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has "
                                + str(cost)
                                + " "
                                + ingredient
                                + "\n "
                                + str(cost2)
                                + " "
                                + ingredient2
                                + "\nand "
                                + str(cost3)
                                + " "
                                + ingredient3
                                + "! ✅\nYou successfully crafted "
                                + output
                                + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                            )
                            save_to_userfile(data, name)
                            print("saved")

                        else:
                            bot.send_message(
                                message.chat.id,
                                " 🛠 CRAFTING 🛠"
                                + output
                                + "!!\n Stash 📦 Available ✅\n@"
                                + name
                                + " has "
                                + str(data["stash"]["stashinv"].count(ingredient))
                                + " "
                                + ingredient
                                + "\n "
                                + str(data["stash"]["stashinv"].count(ingredient2))
                                + " "
                                + ingredient2
                                + "\n And "
                                + str(data["stash"]["stashinv"].count(ingredient3))
                                + " "
                                + ingredient3
                                + " ❌\nTry again when you have the required ingredients! ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            " 🛠 CRAFTING 🛠"
                            + output
                            + "!!\n Stash 📦 Available ✅\n@"
                            + name
                            + " has "
                            + str(data["stash"]["stashinv"].count(ingredient))
                            + " "
                            + ingredient
                            + "\n "
                            + str(data["stash"]["stashinv"].count(ingredient2))
                            + " "
                            + ingredient2
                            + "\n And "
                            + str(data["stash"]["stashinv"].count(ingredient3))
                            + " "
                            + ingredient3
                            + " ❌\nTry again when you have the required ingredients! ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + "\n "
                        + str(data["stash"]["stashinv"].count(ingredient2))
                        + " "
                        + ingredient2
                        + "\n And "
                        + str(data["stash"]["stashinv"].count(ingredient3))
                        + " "
                        + ingredient3
                        + " ❌\nTry again when you have the required ingredients! ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )


@bot.message_handler(commands=["craftwoodspear"])
def craftwoodspear(message):
    name = message.from_user.username
    cost = 1
    ingredient = "Wood Staff"
    type = "rawmaterials"
    output = "Wood Spear"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        if data["stash"]["tools"]["knife"]:
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + " and also has Handy Knife 🔪! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again when you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has no Handy Knife 🔪❌\n\n 🛠❌ CRAFT FAILED  ❌🛠",
                )
        else:
            bot.send_message(
                message.chat.id,
                " 🛠 CRAFTING 🛠"
                + output
                + "!!\n Stash 📦 Not Available ❌\n  @"
                + name
                + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
            )


@bot.message_handler(commands=["craftclaybrick"])
def craftclaybrick(message):
    name = message.from_user.username
    cost = 1
    ingredient = "Red Clay"
    type = "rawmaterials"
    output = "Raw Clay Bricks"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        if data["stash"]["tools"]["woodframe"]:
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + " and also has Brick Making Wood Frame 🖼! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again when you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )
        else:
            bot.send_message(
                message.chat.id,
                " 🛠 CRAFTING 🛠"
                + output
                + "!!\n Stash 📦 Available ✅\n@"
                + name
                + " has no Brick Making Wood Frame 🖼 ❌\n\n 🛠❌ CRAFT FAILED  ❌🛠",
            )


@bot.message_handler(commands=["craftexcrementbrick"])
def craftexcrementbrick(message):
    name = message.from_user.username
    cost = 3
    ingredient = "Excrement"
    type = "rawmaterials"
    output = "Excrement Brick"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        if data["stash"]["tools"]["woodframe"]:
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + " and also has Brick Making Wood Frame 🖼! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again when you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:

                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )
        else:
            bot.send_message(
                message.chat.id,
                " 🛠 CRAFTING 🛠"
                + output
                + "!!\n Stash 📦 Available ✅\n@"
                + name
                + " has no Brick Making Wood Frame 🖼 ❌\n\n 🛠❌ CRAFT FAILED  ❌🛠",
            )


@bot.message_handler(commands=["craftclaydish"])
def craftclaydish(message):
    name = message.from_user.username
    cost = 1
    ingredient = "Red Clay"
    type = "rawmaterials"
    output = "Raw Clay Dish"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        if data["stash"]["stashlevel"] > 0:
            if data["stash"]["stashinv"].count(ingredient) >= cost:
                data["stash"]["stashinv"].remove(ingredient)
                data["stash"]["stashinv"].append(output)
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has "
                    + str(cost)
                    + " "
                    + ingredient
                    + "✅\n@"
                    + name
                    + ", you successfully crafted "
                    + output
                    + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                )
                save_to_userfile(data, name)
                print("saved")
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has "
                    + str(data["stash"]["stashinv"].count(ingredient))
                    + " "
                    + ingredient
                    + " and you need "
                    + str(cost)
                    + " ❌\nTry again when you have more "
                    + ingredient
                    + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                )

        else:
            bot.send_message(
                message.chat.id,
                " 🛠 CRAFTING 🛠"
                + output
                + "!!\n Stash 📦 Not Available ❌\n  @"
                + name
                + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
            )


@bot.message_handler(commands=["craftclaypan"])
def craftclaypan(message):
    name = message.from_user.username
    cost = 1
    ingredient = "Red Clay"
    type = "rawmaterials"
    output = "Raw Clay Pan"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        if data["stash"]["stashlevel"] > 0:
            if data["stash"]["stashinv"].count(ingredient) >= cost:
                data["stash"]["stashinv"].remove(ingredient)
                data["stash"]["stashinv"].append(output)
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has "
                    + str(cost)
                    + " "
                    + ingredient
                    + "✅\n@"
                    + name
                    + ", you successfully crafted "
                    + output
                    + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                )
                save_to_userfile(data, name)
                print("saved")
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has "
                    + str(data["stash"]["stashinv"].count(ingredient))
                    + " "
                    + ingredient
                    + " and you need "
                    + str(cost)
                    + " ❌\nTry again when you have more "
                    + ingredient
                    + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                )
        else:
            bot.send_message(
                message.chat.id,
                " 🛠 CRAFTING 🛠"
                + output
                + "!!\n Stash 📦 Not Available ❌\n  @"
                + name
                + ", you dont have a Stash  📦built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
            )


@bot.message_handler(commands=["craftclayjar"])
def craftclayjar(message):
    name = message.from_user.username
    cost = 1
    ingredient = "Red Clay"
    type = "rawmaterials"
    output = "Raw Clay Jar"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        if data["stash"]["stashlevel"] > 0:
            if data["stash"]["stashinv"].count(ingredient) >= cost:
                data["stash"]["stashinv"].remove(ingredient)
                data["stash"]["stashinv"].append(output)
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has "
                    + str(cost)
                    + " "
                    + ingredient
                    + "✅\n@"
                    + name
                    + ", you successfully crafted "
                    + output
                    + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                )
                save_to_userfile(data, name)
                print("saved")
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has "
                    + str(data["stash"]["stashinv"].count(ingredient))
                    + " "
                    + ingredient
                    + " and you need "
                    + str(cost)
                    + " ❌\nTry again when you have more "
                    + ingredient
                    + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                )
        else:
            bot.send_message(
                message.chat.id,
                " 🛠 CRAFTING 🛠"
                + output
                + "!!\n Stash 📦 Not Available ❌\n  @"
                + name
                + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
            )


@bot.message_handler(commands=["craftclaypot"])
def craftclaypot(message):
    name = message.from_user.username
    cost = 1
    ingredient = "Red Clay"
    type = "rawmaterials"
    output = "Raw Clay Pot"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        if data["stash"]["stashlevel"] > 0:
            if data["stash"]["stashinv"].count(ingredient) >= cost:
                data["stash"]["stashinv"].remove(ingredient)
                data["stash"]["stashinv"].append(output)
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has "
                    + str(cost)
                    + " "
                    + ingredient
                    + "✅\n@"
                    + name
                    + ", you successfully crafted "
                    + output
                    + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                )
                save_to_userfile(data, name)
                print("saved")
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has "
                    + str(data["stash"]["stashinv"].count(ingredient))
                    + " "
                    + ingredient
                    + " and you need "
                    + str(cost)
                    + " ❌\nTry again when you have more "
                    + ingredient
                    + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                )
        else:
            bot.send_message(
                message.chat.id,
                " 🛠 CRAFTING 🛠"
                + output
                + "!!\n Stash 📦 Not Available ❌\n  @"
                + name
                + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
            )


@bot.message_handler(commands=["craftclaybowl"])
def craftclaybowl(message):
    name = message.from_user.username
    cost = 1
    ingredient = "Red Clay"
    type = "rawmaterials"
    output = "Raw Clay Bowl"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        if data["stash"]["stashlevel"] > 0:
            if data["stash"]["stashinv"].count(ingredient) >= cost:
                data["stash"]["stashinv"].remove(ingredient)
                data["stash"]["stashinv"].append(output)
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has "
                    + str(cost)
                    + " "
                    + ingredient
                    + "✅\n@"
                    + name
                    + ", you successfully crafted "
                    + output
                    + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                )
                save_to_userfile(data, name)
                print("saved")
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has "
                    + str(data["stash"]["stashinv"].count(ingredient))
                    + " "
                    + ingredient
                    + " and you need "
                    + str(cost)
                    + " ❌\nTry again when you have more "
                    + ingredient
                    + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                )
        else:
            bot.send_message(
                message.chat.id,
                " 🛠 CRAFTING 🛠"
                + output
                + "!!\n Stash 📦 Not Available ❌\n  @"
                + name
                + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
            )


@bot.message_handler(commands=["craftwoodstaff"])
def craftwoodstaff(message):
    name = message.from_user.username
    cost = 3
    ingredient = "Plain Wood"
    type = "rawmaterials"
    output = "Wood Staff"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        with open("market.json", "r") as f:
            marketData = json.load(f, cls=MarketDecoder)
            tspace = data["stash"]["stashspace"] - len(data["stash"]["stashinv"])
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + "! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again when you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Not Available ❌\n  @"
                    + name
                    + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
                )


@bot.message_handler(commands=["stashout"])
def stashout(message):
    name = message.from_user.username
    data = load_from_userfile(name)
    m = (
        "📦*STASHOUT*📦\n\n*Stash Out* allows you to transfer an item *from your Stash 📦 into a Collectors inventory*. For this, your Collector *needs to be in the same terrain as your personal Stash 📦 is located*.\n\n *COMMAND* \n/stashout <Collector Nr> <Item Nr>\n Replace <Collector Nr> with the number of the Colector you want to give the item to. \nReplace <Item Nr> with the Number of the item. \n\n📦 Current Stash 📦 Inventory: "
        + str(data["stash"]["stashinv"])
        + "\n*Items in Inventories are numbered by the order in which they appear on the List, starting at number one, and from left to right!\n\n End of report 🧐*"
    )

    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, m, parse_mode="Markdown")
    elif len(message.text.split()) == 2:
        bot.send_message(message.chat.id, m, parse_mode="Markdown")
    elif len(message.text.split()) == 3:
        colN = message.text.split()[1]
        colNu = int(colN) - 1
        item = message.text.split()[2]
        itemNu = int(item) - 1
        d = data["collectors"][colNu]
        if d["location"] == data['stash']['stashlocation']:
            if data["stash"]["stashlevel"] > 0:

                item = data["stash"]["stashinv"][itemNu]
                d["inv"].append(item)
                data["stash"]["stashinv"].remove(item)
                save_to_userfile(data, name)
                bot.send_message(
                    message.chat.id,
                    "✅📦*STASHOUT*📦✅\n\n@"
                    + name
                    + ", *your Collector "
                    + str(colN)
                    + " successfully took "
                    + item
                    + " from the Stash 📦 and added it to his inventory!*",
                    parse_mode="Markdown",
                )
            else:
                bot.send_message(
                    message.chat.id,
                    "❌📦*STASHOUT*📦❌\n\n@"
                    + name
                    + ", *you need to build your Stash 📦 Lvl 1 to use this feature*\n📦 *STASH INFO* 📦\n\n*Stash Lvl:* "
                    + str(data["stash"]["stashlevel"])
                    + "\n*Stash Location:* "
                    + data['stash']['stashlocation']
                    + "\n🪵 *Wood Missing:* "
                    + str(data["stash"]["stashmissing"]["woodmissing"])
                    + "\n🪨 *Granite Missing:* "
                    + str(data["stash"]["stashmissing"]["stonemissing"])
                    + "\n🧱*Clay Missing*: "
                    + str(data["stash"]["stashmissing"]["claymissing"])
                    + " \n\n *End of report 🧐*",
                    parse_mode="Markdown",
                )
        else:
            bot.send_message(
                message.chat.id,
                "❌📦*STASHOUT*📦❌\n\n@"
                + name
                + ", *your Collector needs to be in the same terrain as your personal Stash 📦 is located!*",
                parse_mode="Markdown",
            )


@bot.message_handler(commands=["craft"])
def craft(message):
    bot.send_message(
        message.chat.id,
        f" *🛠 CRAFT 🛠* \n\n"
        f"On this game, you are able to use the Items you earn, to craft 🛠 more advanced ones. To do that, "
        f"you need:\n Stash 📦 \n The right ingredients\n And in some case the right tools 🛠!\n\n"
        f"🛠 📃 *Craft List* 📃🛠\n\n *NO TOOLS NEEDED* \n *Weak Rope* ➰ \n Cost : 3 Grass Tuft | "
        f"Command : /craftrope \n *Compost* 💩 \n Cost : 1  Excrement + 2 Dried Leaf | Command : /craftcompost \n"
        f"*Tree Bark Chips* 🌳🍟 \n Cost : 2 Tree Bark | Command : /crafttbchips \n *Fire Place* 🔥 \n"
        f"Cost : 8 Granite Stone | Command : /craftfireplace \n *Wood Fence* \n Cost : 4 Plain Wood | "
        f"Command : /craftfence \n *Excrement Pellet* 💩 \n Cost : 3 Excrement | Command : /craftpellet \n"
        f"*Raw Clay Dish* 🍽 \n Cost : 1 Red Clay | Command : /craftclaydish \n *Raw Clay Pan* 🥘 \n"
        f"Cost : 1 Red Clay | Command : /craftclaypan \n *Raw Clay Pot* 🍯 \n Cost : 1 Red Clay | Command : "
        f"/craftclaypot \n *Raw Clay Jar* 🏺 \n Cost : 1 Red Clay | Command : /craftclayjar \n *Raw Clay Bowl* 🥣 \n"
        f"Cost : 1 Red Clay | Command : /craftclaybowl \n  *Wood Staff* \n Cost : 3 Plain Wood Command : "
        f"/craftwoodstaff \n *Weak Fishing Rod* 🎣 \n Cost : 1 Bone Hook + 2 Plain Wood + 1 Weak Rope | Command : "
        f"/craftfishingrod \n *Weak Bow* 🏹 Cost : 2 Plain Wood + 2 Weak Rope | Command : /craftweakbow \n"
        f"*Stone Axe* 🪓 \n Cost: 2 Plain Wood + 1 Weak Rope + 1 Flat Stone | Command: /craftstoneaxe \n\n"
        f"*TOOLS NEEDED* \n *Raw Clay Brick* 🧱 \n Cost : 1 Red Clay | Tool :   *Brick Making Wood Frame* 🖼 | "
        f"Command : /craftclaybrick \n *Excrement Brick* 💩🧱 \n Cost : 3 Excrement | Tool :   Brick Making Wood "
        f"Frame 🖼 | Command : /craftexcrementbrick \n *Bone Hook* 🎣 \n Cost : 1 Small Bone | Tool :   "
        f"Handy Knife 🔪 | Command : /craftbonehook \n *Brick Making Wood Frame* 🖼  \n Cost : 5 Plain Wood | Tool :   "
        f"Handy Knife 🔪 | Command : /craftwoodframe \n *Wood Spear* \n Cost : 1 Wood Staff | Tool :   "
        f"Handy Knife 🔪 | Command : /craftwoodspear \n *Simple Arrows* 🏹 \n Cost : 1 Plain Wood | Tool :   "
        f"Handy Knife 🔪 | Command : /craftsimplearrows \n *End of report 🧐*",
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["sell"])
def sell(message):
    name = message.from_user.username
    bot.send_message(
        message.chat.id,
        f"🛒         SELL         🛒\n\n"
        f"This game contains a /market that allows you to SELL Items that you earned or crafted. \n"
        f"To Sell any item, you need:\n\nStash 📦 Lvl 1 (min)\n Collectors License 🔖 \n You can check"
        f"the different Supplies with the commands below: \n /foodsupply (check Market Food Supply) \n"
        f"/coinsupply (check Market Coin Supply) \n /rawsupply (check Market Raw Materials Supply) \n\n"
        f"Using the commands above will display info on the item Count and Price on the Market. More will"
        f"be added soon!\n\n /market will display all the commands to buy or sell!",
    )


@bot.message_handler(commands=["buy"])
def buy(message):
    name = message.from_user.username
    bot.send_message(
        message.chat.id,
        f"🛒         BUY         🛒\n\n"
        f"This game contains a /market that allows you to BUY Items that it contains in stock. \n"
        f"To buy you only need: \n\n Enough Coins 💰 \n Stash 📦 Lvl 1 or Better. \n"
        f"You can check the different Supplies with the commands below: \n /foodsupply (check Market Food Supply) \n"
        f"/coinsupply (check Market Coin Supply) \n /rawsupply (check Market Raw Materials Supply) \n\n"
        f"Using the commands above will display info on the item Count and Price on the Market. More will "
        f"be added soon!\n\n /market will display all the commands to buy or sell!",
    )


@bot.message_handler(commands=["wo"])
def wo(message):
    name = message.from_user.username
    if name == "Funkaclau":
        uName = message.text.split()[1]
        action = message.text.split()[2]
        mod = message.text.split()[3]
        colN = int(message.text.split()[4])
        number = message.text.split()[5]

        with open(uName + ".json", "r") as f:
            data = json.load(f, cls=UserDecoder)
            d = data["collectors"][colN]
            bot.send_message(message.chat.id, d)
            if action == "poder":
                if mod == "+":
                    data['foodBank'] += int(number)
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                        bot.send_message(message.chat.id, dataS)
                elif mod == "-":
                    data['foodBank'] -= int(number)
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                        bot.send_message(message.chat.id, dataS)


@bot.message_handler(commands=["wt"])
def wt(message):
    name = message.from_user.username
    if name == "Funkaclau":
        uName = message.text.split()[1]
        mod = message.text.split()[2]
        colN = int(message.text.split()[3])
        number = message.text.split()[4]
        print(number)
        with open(uName + ".json", "r") as f:
            data = json.load(f, cls=UserDecoder)
            d = data["collectors"][colN]
            if number == "false":
                if mod == "tele":
                    d["gear"]["tele"] = False
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                    f.write(dataS)
                elif mod == "bota":
                    d["gear"]["boots"] = False
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                elif mod == "cinto":
                    d["gear"]["belt"] = False
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                elif mod == "trevo":
                    d["gear"]["clover"] = False
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                elif mod == "bolsa":
                    d["gear"]["bag"] = False
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                elif mod == "machado":
                    d["gear"]["axe"] = False
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                elif mod == "picareta":
                    d["gear"]["pick"] = False
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
            elif number == "true":
                if mod == "tele":
                    d["gear"]["tele"] = True
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                    f.write(dataS)
                elif mod == "bota":
                    d["gear"]["boots"] = True
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                elif mod == "cinto":
                    d["gear"]["belt"] = True
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                elif mod == "trevo":
                    d["gear"]["clover"] = True
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                elif mod == "bolsa":
                    d["gear"]["bag"] = True
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                elif mod == "machado":
                    d["gear"]["axe"] = True
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)
                elif mod == "picareta":
                    d["gear"]["pick"] = True
                    with open(uName + ".json", "w") as f:
                        dataS = json.dumps(data, indent=4)
                        f.write(dataS)


@bot.message_handler(commands=["manifest"])
def manifest(message):
    name = message.from_user.username
    if name == "Funkaclau":
        uName = message.text.split()[1]
        address = message.text.split()[2]

        with open("jsontemp.json", "r") as f:
            data = json.load(f, cls=UserDecoder)
            data["name"] = uName
            data["wallet"] = address
            data["collectors"][0]["owner"] = uName
            with open(uName + ".json", "a+") as f:

                dataS = json.dumps(data, indent=4)
                print(dataS)
                f.write(dataS)


@bot.message_handler(commands=["manifestCol"])
def manifestCol(message):
    name = message.from_user.username
    if name == "Funkaclau":
        uName = message.text.split()[1]
        number = int(message.text.split()[2])
        with open("coljsontemp.json", "r") as f:
            data = json.load(f, cls=UserDecoder)
            data["owner"] = uName
            with open(uName + ".json", "a+") as g:
                # dataPlayer = json.load(f, cls=UserDecoder)
                dataS = json.dumps(data, indent=4)
                dataP = json.load(g, cls=UserDecoder)
                while number > 0:

                    dataP["collectors"].append(", " + dataS)
                    number -= 1


@bot.message_handler(commands=["craftsimplearrows"])
def craftsimplearrows(message):
    name = message.from_user.username
    cost = 1
    ingredient = "Plain Wood"
    type = "rawmaterials"
    output = "Simple Arrows"
    with open(name + ".json", "r") as f:
        data = json.load(f, cls=UserDecoder)
        if data["stash"]["tools"]["knife"]:
            if data["stash"]["stashlevel"] > 0:
                if data["stash"]["stashinv"].count(ingredient) >= cost:
                    data["stash"]["stashinv"].remove(ingredient)
                    data["stash"]["stashinv"].append(output)
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(cost)
                        + " "
                        + ingredient
                        + " and also has Handy Knife 🔪! ✅\n@"
                        + name
                        + ", you successfully crafted "
                        + output
                        + "\n\n 🛠✅ CRAFT SUCCESSFUL  ✅🛠",
                    )
                    save_to_userfile(data, name)
                    print("saved")
                else:
                    bot.send_message(
                        message.chat.id,
                        " 🛠 CRAFTING 🛠"
                        + output
                        + "!!\n Stash 📦 Available ✅\n@"
                        + name
                        + " has "
                        + str(data["stash"]["stashinv"].count(ingredient))
                        + " "
                        + ingredient
                        + " and you need "
                        + str(cost)
                        + " ❌\nTry again when you have more "
                        + ingredient
                        + ". ❌ \n\n 🛠❌ CRAFT FAILED  ❌🛠",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    " 🛠 CRAFTING 🛠"
                    + output
                    + "!!\n Stash 📦 Available ✅\n@"
                    + name
                    + " has no Handy Knife 🔪❌\n\n 🛠❌ CRAFT FAILED  ❌🛠",
                )
        else:
            bot.send_message(
                message.chat.id,
                " 🛠 CRAFTING 🛠"
                + output
                + "!!\n Stash 📦 Not Available ❌\n  @"
                + name
                + ", you dont have a Stash 📦 built yet, therefore you can´t craft. ❌ \n\n 🛠❌ CRAFT FAILED ❌🛠",
            )


@bot.message_handler(commands=["depositfood"])
def bot_depositfood(message):
    name = message.from_user.username
    print(f"{name} {message.text}")
    data = load_from_userfile(name)
    calories = count_calories(data["wallet"])
    if calories > 0:
        data['foodBank'] += calories
        save_to_userfile(data, name)
        bot.send_message(
            message.chat.id,
            f"Successfully deposited: {calories} Calories.\n"
            f"Your total calories amount is now: {data['foodBank']} Calories.",
        )
    else:
        bot.send_message(
            message.chat.id,
            f'There is no new transfers with Memo: "{MEMO}" found.\n'
            f'Please send some food to "`{RECIPIENT}`" with Memo: "`{MEMO}`".\n'
            f"You can do it using [this link]"
            f"(https://wax.atomichub.io/trading/transfer?partner=pixeltycoons&memo={MEMO}).\n"
            f"Your total calories amount is: {data['foodBank']} Calories.",
            parse_mode="MARKDOWN",
            disable_web_page_preview=True,
        )


# If enough Add count
def exploreC(data, message, name):
    number = 0
    if data["exploreC"] == 5:
        number = 1
    elif data["exploreC"] == 15:
        number = 2
    elif data["exploreC"] == 30:
        number = 3
    elif data["exploreC"] == 50:
        number = 4
    elif data["exploreC"] == 100:
        number = 5
    if number > 0:
        data["ccoins"] += number
        bot.send_message(
            message.chat.id,
            f"🥳🎉Congratz🎉🥳\n\n"
            f"@{name}! You explored your {data['exploreC']}th time.\n"
            f"You earned {number}Coin/s 🪙! \nCoins : {data['ccoins']}\n"
            f"Keep it up!",
        )


def searchC(data, message, name):
    number = 0
    if data["searchC"] == 5:
        number = 1
    elif data["searchC"] == 15:
        number = 2
    elif data["searchC"] == 30:
        number = 3
    elif data["searchC"] == 50:
        number = 4
    elif data["searchC"] == 100:
        number = 5
    if number > 0:
        data["ccoins"] += number
        bot.send_message(
            message.chat.id,
            f"🥳🎉Congratz🎉🥳\n\n"
            f"@{name}! You searched your {data['searchC']}th time.\n"
            f"You earned {number}Coin/s 🪙! \nCoins : {data['ccoins']}\n"
            f"Keep it up!",
        )


def homeC(data, message, name):
    number = 0
    if data["homeC"] == 5:
        number = 1
    elif data["homeC"] == 15:
        number = 2
    elif data["homeC"] == 30:
        number = 3
    elif data["homeC"] == 50:
        number = 4
    elif data["homeC"] == 100:
        number = 5
    if number > 0:
        data["ccoins"] += number
        bot.send_message(
            message.chat.id,
            f"🥳🎉Congratz🎉🥳\n\n"
            f"@{name}! You used /home for the {data['homeC']}th time. \n"
            f"You earned {number}Coin/s 🪙! \nCoins : {data['ccoins']}\n"
            f"Keep it up!",
        )


def chopC(data, message, name):
    number = 0
    if data["chopC"] == 5:
        number = 1
    elif data["chopC"] == 15:
        number = 2
    elif data["chopC"] == 30:
        number = 3
    elif data["chopC"] == 50:
        number = 4
    elif data["chopC"] == 100:
        number = 5
    if number > 0:
        data['ccoins'] += number
        bot.send_message(
            message.chat.id,
            f"🥳🎉Congratz🎉🥳\n\n"
            f"@{name}! You chopped for the {data['chopC']}th time. \n"
            f"You earned {number} Coin/s 🪙! \nCoins : {data['ccoins']}\n"
            f"Keep it up!",
        )


def mineC(data, message, name):
    number = 0
    if data["mineC"] == 5:
        number = 1
    elif data["mineC"] == 15:
        number = 2
    elif data["mineC"] == 30:
        number = 3
    elif data["mineC"] == 50:
        number = 4
    elif data["mineC"] == 100:
        number = 5
    if number > 0:
        data['ccoins'] += number
        bot.send_message(
            message.chat.id,
            f"🥳🎉Congratz🎉🥳\n\n"
            f"@{name}! You mined for the {data['mineC']}th time. \n"
            f"You earned {number} Coin/s 🪙! \nCoins : {data['ccoins']}\n"
            f"Keep it up!",
        )


# Clover checks
def cloverExplore(d, data, message, name):
    if d["gear"]["clover"]:
        chance = randint(0, 5)
        if chance == 0:
            data["collectedC"] += 2
            # moraleUp(d, data, message, name)
            bot.send_message(
                message.chat.id,
                "Clover 🍀=✅\n\n🎲=✅\n@"
                + name
                + " Collector "
                + str(d["number"])
                + " got really Lucky with his Clover 🍀! Double Drop Incoming... \n 🍀!\n🎲=✅",
            )
            drops(d, data, message, name)
        else:
            data["collectedC"] += 1
            bot.send_message(
                message.chat.id,
                "Clover 🍀=✅\n\n🎲=❌\n\n@"
                + name
                + " collector"
                + str(d["number"])
                + "  wasn't lucky with his clover 🍀 this time!\n",
            )
    else:
        bot.send_message(
            message.chat.id,
            "Clover 🍀=❌\n\n@"
            + name
            + " Collector "
            + str(d["number"])
            + " doesn't own a Clover 🍀.\n\n 🍀=❌",
        )
        data["collectedC"] += 1


def cloverSearch(d, data, message, name):
    if d["gear"]["clover"]:
        chance = randint(0, 5)
        if chance == 0:
            # moraleUp(d, data, message, name)
            data["collectedC"] += 4
            bot.send_message(
                message.chat.id,
                "Clover 🍀=✅\n\n🎲=✅\n@"
                + name
                + " Collector "
                + str(d["number"])
                + " got really Lucky with his Clover🍀! Double Drop Incoming... \n 🍀!\n🎲=✅",
            )
            dropsSearch(d, data, message, name)

        else:
            bot.send_message(
                message.chat.id,
                "Clover 🍀=✅\n\n🎲=❌\n@"
                + name
                + " Collector "
                + str(d["number"])
                + " wasn't lucky with his Clover  🍀 this time!\n\n🎲=❌",
            )
            data["collectedC"] += 2
    else:
        bot.send_message(
            message.chat.id,
            "Clover🍀=❌\n\n@"
            + name
            + " Collector "
            + str(d["number"])
            + "  doesn't own a Clover 🍀.\n\n 🍀=❌",
        )
        data["collectedC"] += 2


def cloverMine(d, data, message, name):
    if d["gear"]["clover"]:
        chance = randint(0, 5)
        if chance == 0:
            # moraleUp(d, data, message, name)
            bot.send_message(
                message.chat.id,
                f"Clover 🍀=✅\n\n🎲=✅\n@{name}, Collector {d['number']} got really Lucky with his Clover 🍀!"
                f"Double Drop Incoming... \n 🍀!\n🎲=✅",
            )
            data["collectedC"] += 4
            mine(d, data, message, name)
            mine(d, data, message, name)
        else:
            bot.send_message(
                message.chat.id,
                f"Clover 🍀=✅\n\n"
                f"🎲=❌\n@{name}, Collector {d['number']} wasn't lucky with his clover 🍀 this time!\n\n🎲=❌",
            )
            data["collectedC"] += 2
    else:
        bot.send_message(
            message.chat.id,
            f"Clover 🍀=❌\n\n@{name}, Collector {d['number']} doesn't own a Clover 🍀. \n\n 🍀=❌",
        )
        data["collectedC"] += 2


def cloverChop(d, data, message, name):
    if d["gear"]["clover"]:
        chance = randint(0, 5)
        if chance == 0:
            # moraleUp(d, data, message, name)
            bot.send_message(
                message.chat.id,
                f"Clover 🍀=✅\n\n🎲=✅\n@{name}, Collector {d['number']} got really Lucky with his Clover 🍀!"
                f"Double Drop Incoming... \n 🍀!\n🎲=✅",
            )
            chop(d, data, message, name)
        else:
            bot.send_message(
                message.chat.id,
                f"Clover 🍀=✅\n\n"
                f"🎲=❌\n@{name}, Collector {d['number']} wasn't lucky with his clover 🍀 this time!\n\n🎲=❌",
            )
    else:
        bot.send_message(
            message.chat.id,
            f"Clover 🍀=❌\n\n@{name}, Collector {d['number']} doesn't own a Clover 🍀. \n\n 🍀=❌",
        )


def teleportal(d, data, message, name):
    if d["gear"]["tele"]:
        bot.send_message(
            message.chat.id,
            f"🔮 TELEPORTING 🔮\n\n @{name} Collector {d['number']} is teleporting 🔮✅:\n\n{d['inv']}",
        )
        data["nftout"].append(d["inv"])
        d["inv"] = []

        save_to_userfile(data, name)
        with open("nftout.json", "a") as f:
            f.write(name + ", ")
    else:
        bot.send_message(
            message.chat.id,
            f" 🔮= ❌\n\n@{name}, Your collector {d['number']} doesnt have a Teleportal 🔮 Equipped",
        )


def chop(d, data, message, name):
    d["inv"].append("Plain Wood")
    d["inv"].append("Plain Wood")
    bot.send_message(
        message.chat.id,
        f"🎁\n\n@{name}, your Collector {d['number']} chopped 2 Wood\n 🪓🪵🪵",
    )
    save_to_userfile(data, name)


def bootsChop(d, data, message, name):
    ## Boots Branch
    if d["gear"]["boots"]:
        data['foodBank'] -= 47
        print("- 47")
        cloverChop(d, data, message, name)
        chop(d, data, message, name)

        ## No Boots Branch
    else:
        data['foodBank'] -= 50
        print("- 50")
        cloverChop(d, data, message, name)
        # drops(d, data)
        chop(d, data, message, name)


def bootsMine(d, data, message, name):
    ## Boots Branch
    if d["gear"]["boots"]:
        data['foodBank'] -= 47
        print("- 47")
        cloverMine(d, data, message, name)
        mine(d, data, message, name)
        mine(d, data, message, name)

        ## No Boots Branch
    else:
        data['foodBank'] -= 50
        print("- 50")
        cloverMine(d, data, message, name)
        # drops(d, data)
        mine(d, data, message, name)
        mine(d, data, message, name)


def beltChop(d, data, message, name):
    if len(d["inv"]) > d["maxinv"]:
        bot.send_message(
            message.chat.id,
            "⚠️⚠️⚠️\n\n@"
            + name
            + " Collector "
            + str(d["number"])
            + " is currently overburdened.\n This means he has more inventory than what he can carry. His current maximum is "
            + str(d["maxinv"])
            + " items. \n use the command /drop <collector number> <item you want to drop>\n\nIf your collector has a Teleportal 🔮 equipped, then you can use:\n/teleport <Collector Number> to withdraw and receive your rewards next Monday",
        )
    elif d["gear"]["belt"]:
        chance = randint(0, 7)
        ## Free Move branch
        if chance == 7:
            print("free move")
            bot.send_message(
                message.chat.id,
                "Belt=✅\n🎲=✅\n@"
                + name
                + " Collector "
                + str(d["number"])
                + " 🠠belt shined mysteriously and you performed this action without spending energy!\n✅",
            )
            # moraleUp(d, data, message, name)
            cloverChop(d, data, message, name)
            chop(d, data, message, name)
            print(d)
        else:
            print("no luck with belt")
            bot.send_message(
                message.chat.id,
                "Belt=✅\n🎲=❌\n@"
                + name
                + " Collector "
                + str(d["number"])
                + " belt hadn't shined this time!\n❌",
            )
            bootsChop(d, data, message, name)
    else:
        bot.send_message(
            message.chat.id,
            "Belt=❌\n\n@"
            + name
            + " Collector "
            + str(d["number"])
            + " has no belt!\n❌",
        )
        bootsChop(d, data, message, name)


def beltMine(d, data, message, name):
    if len(d["inv"]) > d["maxinv"]:
        bot.send_message(
            message.chat.id,
            "⚠️⚠️⚠️\n\n@"
            + name
            + " Collector "
            + str(d["number"])
            + " is currently overburdened.\n This means he has more inventory than what he can carry. His current maximum is "
            + str(d["maxinv"])
            + " items. \n use the command /drop <collector number> <item you want to drop>\n\nIf your collector has a Teleportal 🔮 equipped, then you can use:\n/teleport <Collector Number> to withdraw and receive your rewards next Monday",
        )
    elif d["gear"]["belt"]:
        chance = randint(0, 7)
        ## Free Move branch
        if chance == 7:
            print("free move")
            bot.send_message(
                message.chat.id,
                "Belt=✅\n🎲=✅\n\n@"
                + name
                + ", your Collector "
                + str(d["number"])
                + " belt shined mysteriously and you performed this action without spending energy!✅",
            )
            cloverMine(d, data, message, name)
            mine(d, data, message, name)
            mine(d, data, message, name)
            # moraleUp(d, data, message, name)
            print(d)
        else:
            print("no luck with belt")
            bot.send_message(
                message.chat.id,
                "Belt=✅\n🎲=❌\n\n@"
                + name
                + ", your Collector "
                + str(d["number"])
                + " belt hadn't shined this time!❌",
            )
            bootsMine(d, data, message, name)
    else:
        bot.send_message(
            message.chat.id,
            "Belt=❌\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has no belt!❌",
        )
        bootsMine(d, data, message, name)


# belt check
def belt(d, data, message, name):
    if len(d["inv"]) > d["maxinv"]:
        bot.send_message(
            message.chat.id,
            "⚠️🚶‍♂️ EXPLORE 🚶‍♂️⚠️\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is currently overburdened.\n This means he has more inventory than what he can carry. His current maximum is 3 items. \n use the command /drop <collector number> <item you want to drop>\n\nIf your collector has a Teleportal 🔮 equipped, then you can use:\n/teleport <Collector Number> to withdraw and receive your rewards next Monday",
        )

    elif d["gear"]["belt"]:
        chance = randint(0, 7)
        ## Free Move branch
        if chance == 7:
            # moraleUp(d, data, message, name)
            print("free move")
            bot.send_message(
                message.chat.id,
                "🚶‍♂️ EXPLORE 🚶‍♂️\nBelt=✅\n🎲=✅\n@"
                + name
                + ", your Collector "
                + str(d["number"])
                + " belt shined mysteriously and you performed this action without spending energy!✅",
            )
            cloverExplore(d, data, message, name)
            drops(d, data, message, name)
            print(d)
        else:
            print("no luck with belt")
            bot.send_message(
                message.chat.id,
                "🚶‍♂️ EXPLORE 🚶‍♂️\nBelt=✅\n🎲=❌\n@"
                + name
                + ", your Collector "
                + str(d["number"])
                + " belt hadn't shined this time!❌",
            )
            boots(d, data, message, name)
    else:
        bot.send_message(
            message.chat.id,
            "🚶‍♂️ EXPLORE 🚶‍♂️\nBelt=❌\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has no belt!❌",
        )
        boots(d, data, message, name)


def beltSearch(d, data, message, name):
    if len(d["inv"]) > d["maxinv"]:
        bot.send_message(
            message.chat.id,
            "⚠️🔎 SEARCH 🔍⚠️\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is currently overburdened.\n This means he has more inventory than what he can carry. His current maximum is 3 items. \n use the command /drop <collector number> <item you want to drop>\n\nIf your collector has a Teleportal 🔮 equipped, then you can use:\n/teleport <Collector Number> to withdraw and receive your rewards next Monday",
        )
    elif d["gear"]["belt"]:
        chance = randint(0, 7)
        ## Free Move branch
        if chance == 7:
            print("free move")
            # moraleUp(d, data, message, name)
            bot.send_message(
                message.chat.id,
                "🔎 SEARCH 🔍\nBelt=✅\n🎲=✅\n@"
                + name
                + ", your Collector "
                + str(d["number"])
                + " belt shined mysteriously and you performed this action without spending energy!✅",
            )
            cloverSearch(d, data, message, name)
            dropsSearch(d, data, message, name)
            print(d)
        else:
            print("no luck with belt")
            bot.send_message(
                message.chat.id,
                "🔎 SEARCH 🔍\nBelt=✅\n🎲=❌\n@"
                + name
                + ", your Collector "
                + str(d["number"])
                + " belt hadn't shined this time! ❌",
            )
            bootsSearch(d, data, message, name)
    else:
        bot.send_message(
            message.chat.id,
            "🔎 SEARCH 🔍\nBelt=❌\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has no belt!❌",
        )
        bootsSearch(d, data, message, name)


def beltHome(d, data, message, name):
    if len(d["inv"]) > d["maxinv"]:
        bot.send_message(
            message.chat.id,
            "⚠️🏘 HOME 🏘⚠️\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is currently overburdened.\n This means he has more inventory than what he can carry. His current maximum is 3 items. \n use the command /drop <collector number> <item you want to drop>\n\nIf your collector has a Teleportal 🔮 equipped, then you can use:\n/teleport <Collector Number> to withdraw and receive your rewards next Monday",
        )

    elif d["gear"]["belt"]:
        chance = randint(0, 7)
        ## Free Move branch
        if chance == 7:
            print("free move")
            # moraleUp(d, data, message, name)
            bot.send_message(
                message.chat.id,
                "🏘 HOME 🏘\nBelt=✅\n🎲=✅\@"
                + name
                + ", your Collector "
                + str(d["number"])
                + " belt shined mysteriously and you performed this action without spending energy!✅",
            )
            returnHome(d, data, message, name)
            print(d)
        else:
            print("no luck with belt")
            bot.send_message(
                message.chat.id,
                "🏘 HOME 🏘\nBelt=✅\n🎲=❌\@"
                + name
                + ", your Collector "
                + str(d["number"])
                + " belt hadn't shined this time!❌",
            )
            bootsHome(d, data, message, name)
    else:
        bot.send_message(
            message.chat.id,
            "🏘 HOME 🏘\nBelt=❌\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has no belt!❌",
        )
        bootsHome(d, data, message, name)


def mine(d, data, message, name):
    chance = randint(0, 9)
    if chance < 5:
        d["inv"].append("Granite Stone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " mined 1 Granite Stone 🪨",
        )
        save_to_userfile(data, name)
    elif chance == 5:
        d["inv"].append("Copper Ore")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " mined 1 Copper Ore 🪨",
        )
    elif 6 <= chance <= 7:
        d["inv"].append("Zinc Ore")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + "  your Collector "
            + str(d["number"])
            + " mined 1 Zinc Ore 🪨 ",
        )
        save_to_userfile(data, name)
    else:
        d["inv"].append("Tin Ore")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " mined 1 Tin Ore 🪨",
        )
        save_to_userfile(data, name)


def invP(data, message, name):
    m = (
        "\n\n 👤 User Info 👤\n\nName: "
        + name
        + "\nWallet: "
        + data["wallet"]
        + "\nCoins: "
        + str(data["ccoins"])
        + "\nFood Bank: "
        + str(data["foodBank"])
        + "Calories\nCollector License: "
        + str(data["collectorlicense"])
        + "\nExplore Count: "
        + str(data["exploreC"])
        + "\nSearch Count: "
        + str(data["searchC"])
        + "\nHome Count: "
        + str(data["homeC"])
        + "\nChop Count: "
        + str(data["chopC"])
        + "\nMine Count: "
        + str(data["mineC"])
        + "\nItems Collected: "
        + str(data["collectedC"])
        + "\n\n🧑‍🎤 Collectors🧑‍🎤\n\n Total Collectors: "
        + str(len(data["collectors"]))
        + "\n\n 📦 STASH INFO 📦\n\nStash Location: "
        + str(data['stash']['stashlocation'])
        + "\n\nStash Level: "
        + str(data["stash"]["stashlevel"])
        + "\nStash Total Space: "
        + str(data["stash"]["stashspace"])
        + "\n🌌 Current Space: "
        + str((data["stash"]["stashspace"] - int(len(data["stash"]["stashinv"]))))
        + "\n📦 Stash Inventory: "
        + str(data["stash"]["stashinv"])
        + "\n\nEnd of report 🧐✅"
    )
    # \n\n🛖 HUT INFO 🛖\n\nHut Level: " + str(data["stash"]["hut"]["hutlevel"]) + "\nInstalled:\nFireplace🔥 : " + str(data["stash"]["hut"]["instal"]["fireplace"]) + "\nMud Furnace ♨️: " + str(data["stash"]["hut"]["instal"]["mudfurnace"]) + "\nMattress: " + str(data["stash"]["hut"]["instal"]["mattress"]) + "\nPillow: " + str(data["stash"]["hut"]["instal"]["pillow"]) + "\nGrinder: " + str(data["stash"]["hut"]["instal"]["grinder"]) + "\nTable: " + str(data["stash"]["hut"]["instal"]["table"]) + "\nCompostbin: " + str(data["stash"]["hut"]["instal"]["compostbin"]) + "\n💐 Garden 💐\nCactus: " + str(data["stash"]["hut"]["instal"]["garden"]["cactus"]) + "
    bot.send_message(message.chat.id, m)
    print(m)


def inv(d, data, message, name):
    if len(message.text.split()) == 2:
        colN = message.text.split()[1]
        colNu = int(colN) - 1

        d = data["collectors"][colNu]
        m = (
            "✅ Stats ✅\n\n🚶‍♂️Collector Nr: "
            + str(d["number"])
            + "\n Daring: "
            + str(d["daring"])
            + "\n 🔋 Actions this week: "
            + str(d["actions"])
            + "\n Max Actions: "
            + str(d["actionsMax"])
            + "\n🗺 Collector Location: "
            + d["location"]
            + "\n 🏘 Moves from Home: "
            + str(d["distance"])
            + "\n\nMax Inventory: "
            + str(d["maxinv"])
            + "\n👨‍💻 Inventory: "
            + str(d["inv"])
            + "\n\n🛠 GEAR 🛠\n💫 Belt: "
            + str(d["gear"]["belt"])
            + "\n🍀 Clover: "
            + str(d["gear"]["clover"])
            + "\n 🔮 Teleportal: "
            + str(d["gear"]["tele"])
            + "\n 🎒 Bag: "
            + str(d["gear"]["bag"])
            + "\n 🥾 Boots: "
            + str(d["gear"]["boots"])
            + "\n 🪓 Axe: "
            + str(d["gear"]["axe"])
            + "\n ⛏ Pickaxe: "
            + str(d["gear"]["pick"])
            + "\n\nEnd of report 🧐✅"
        )
        bot.send_message(message.chat.id, m)
        print(m)


def plainE(d, data, message, name):
    chance = randint(0, 199)
    print(chance)
    if chance <= 19:
        d["inv"].append("Seed")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector"
            + str(d["number"])
            + " has found a Seed 🌱",
        )
    elif 20 <= chance <= 69:
        print("got Grass Tuft")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Grass Tuft 🌿",
        )
        d["inv"].append("Grass Tuft")
    elif 70 <= chance <= 99:
        print("got Dried Leaf")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Dried Leaf 🍁",
        )
        d["inv"].append("Dried Leaf")
    elif 100 <= chance <= 124:
        print("got Berries")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector"
            + str(d["number"])
            + " has found Wild Berries 🫐",
        )
        d["inv"].append("Wild Berries")
    elif 125 <= chance <= 149:
        print("excrement")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your collector "
            + str(d["number"])
            + " has found an Excrement 💩",
        )
        d["inv"].append("Excrement")
    elif 150 <= chance <= 174:
        print("Rag")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Rag 📃",
        )
        d["inv"].append("Rag")
    elif chance >= 175:
        print("Bone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Small Bone 🦴",
        )
        d["inv"].append("Small Bone")
    else:
        print("oh shit")


def woodlandE(d, data, message, name):
    chance = randint(0, 99)
    print(chance)
    if chance <= 14:
        d["inv"].append("Dried Leaf")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Dried Leaf 🍁",
        )
        print("Leaf")
    elif 15 <= chance <= 29:
        print("got Plain Wood")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found Wood 🪵",
        )
        d["inv"].append("Plain Wood")
    elif 30 <= chance <= 34:
        print("got Pinecone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Pinecone 🌲",
        )
        d["inv"].append("Pinecone")
    elif 35 <= chance <= 44:
        print("got Tree Bark")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Tree Bark 🌳",
        )
        d["inv"].append("Tree Bark")
    elif 45 <= chance <= 54:
        print("Orange")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found an Orange 🍊",
        )
        d["inv"].append("Orange")
    elif 55 <= chance <= 69:
        print("Grass Tuft")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Grass Tuft 🌿",
        )
        d["inv"].append("Grass Tuft")
    elif 70 <= chance <= 74:
        print("Bone")
        bot.send_message(
            message.chat.id, "🎁\n\n@" + name + " collecto has found a Small Bone 🦴"
        )
        d["inv"].append("Small Bone")
    elif 75 <= chance <= 84:
        print("Excrement")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found an Excrement 💩",
        )
        d["inv"].append("Excrement")
    elif 85 <= chance <= 89:
        print("Fig")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Fig 🍐",
        )
        d["inv"].append("Fig")
    elif 90 <= chance <= 94:
        print("Wild Berries")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Wild Berries 🫐",
        )
        d["inv"].append("Wild Berries")
    elif 95 <= chance <= 99:
        print("Rag")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Rag 📃",
        )
        d["inv"].append("Rag")
    else:
        print("oh shit")


def forestE(d, data, message, name):
    chance = randint(0, 99)
    print(chance)
    if chance <= 14:
        d["inv"].append("Dried Leaf")
        print("leaf")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Dried Leaf 🍁",
        )
    elif 15 <= chance <= 29:
        print("got Plain Wood")
        d["inv"].append("Plain Wood")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found Wood 🪵",
        )
    elif 30 <= chance <= 34:
        print("got Pinecone")
        d["inv"].append("Pinecone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Pinecone 🌲",
        )
    elif 35 <= chance <= 44:
        print("got Tree Bark")
        d["inv"].append("Tree Bark")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Tree Bark 🌳",
        )
    elif 45 <= chance <= 54:
        print("Orange")
        d["inv"].append("Orange")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Orange 🍊",
        )
    elif 55 <= chance <= 59:
        print("Bone")
        d["inv"].append("Small Bone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Small Bone 🦴",
        )
    elif 60 <= chance <= 69:
        print("Excrement")
        d["inv"].append("Excrement")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Excrement 💩",
        )
    elif 70 <= chance <= 76:
        print("Fig")
        d["inv"].append("Fig")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Fig 🍐",
        )
    elif 77 <= chance <= 83:
        print("G mush")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Green Mushroom 🟢🍄",
        )
        d["inv"].append("Green Mushroom")
    elif 84 <= chance <= 90:
        print("Wild Berries")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found Wild Berries 🫐",
        )
        d["inv"].append("Wild Berries")
    elif 91 <= chance <= 99:
        print("Rag")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Rag 📃",
        )
        d["inv"].append("Rag")
    else:
        print("oh shit")


def rockyE(d, data, message, name):
    chance = randint(0, 99)
    print(chance)
    if chance <= 14:
        d["inv"].append("Granite Stone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Granite Stone 🪨",
        )
        print("granite")
    elif 15 <= chance <= 24:
        print("got whitestone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Whitestone 🪨",
        )
        d["inv"].append("Whitestone")
    elif 25 <= chance <= 34:
        print("got Small Bone")
        d["inv"].append("Small Bone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Small Bone 🦴",
        )
    elif 35 <= chance <= 44:
        print("got Excrement")
        d["inv"].append("Excrement")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found an Excrement 💩",
        )
    elif 45 <= chance <= 54:
        print("Egg")
        d["inv"].append("Seagull Egg")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Seagull Egg 🥚",
        )

    elif 55 <= chance <= 59:
        print("Barb Fig")
        d["inv"].append("Barbary Fig")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Barbary Fig 🫒",
        )
    elif 60 <= chance <= 69:
        print("Cactus")
        d["inv"].append("Small Cactus")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Small Cactus 🌵",
        )
    elif 70 <= chance <= 84:
        print("Gravel")
        d["inv"].append("Gravel")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found Gravel 🪨",
        )
    elif 85 <= chance <= 87:
        print("Whetstone")
        d["inv"].append("Whetstone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Whetstone 🪨",
        )
    elif 88 <= chance <= 92:
        print("Rag")
        d["inv"].append("Rag")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Rag 📃",
        )
    elif 93 <= chance <= 99:
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Big Stone 🪨",
        )
        print("Big Stone")
        d["inv"].append("Big Flat Stone")
    else:
        print("oh shit")


def beachE(d, data, message, name):
    chance = randint(0, 99)
    print(chance)
    if chance <= 24:
        d["inv"].append("Drift Wood")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found Drift Wood 🪵",
        )
        print("drift wood")

    elif 25 <= chance <= 44:
        print("got shell")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Shell 🐚",
        )
        d["inv"].append("Shell")
    elif 45 <= chance <= 64:
        print("got flat stone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Flat Stone 🪨",
        )
        d["inv"].append("Flat Stone")

    elif 65 <= chance <= 69:
        print("got Clam")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Clam 🐚",
        )
        d["inv"].append("Clam")

    elif 70 <= chance <= 79:
        print("Rag")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Rag 📃",
        )
        d["inv"].append("Rag")

    elif chance >= 80:
        print("S water")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found Salty Water 💧",
        )
        d["inv"].append("Salty Water")
    else:
        print("oh shit")

        ##############


def plainS(d, data, message, name):
    chance = randint(0, 99)
    print(chance)
    if chance <= 9:
        d["inv"].append("Seed")
        print("Seed")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Seed... 🌱",
        )
    elif 10 <= chance <= 34:
        print("got Grass Tuft")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Grass Tuft... 🌿",
        )
        d["inv"].append("Grass Tuft")
    elif 35 <= chance <= 49:
        print("got Dried Leaf")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Dried Leaf... 🍁",
        )
        d["inv"].append("Dried Leaf")

    elif 50 <= chance <= 59:
        print("got Berries")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found Wild Berries... 🫐",
        )
        d["inv"].append("Wild Berries")
    elif 60 <= chance <= 69:
        print("excrement")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Excrement... 💩",
        )
        d["inv"].append("Excrement")

    elif 70 <= chance <= 79:
        print("Rag")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rag... 📃",
        )
        d["inv"].append("Rag")

    elif 80 <= chance <= 89:
        print("Bone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Small Bone... 🦴",
        )
        d["inv"].append("Small Bone")

    elif 90 <= chance <= 95:
        print("Rusty Nail")
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rusty Nail... 🪡",
        )
        d["inv"].append("Rusty Nail")

    elif chance >= 96:
        print("Rusty Needle")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rusty Needle... 🪡",
        )
        d["inv"].append("Rusty Needle")
    else:
        bot.send_message(
            message.chat.id,
            "🎁\n\n@" + name + " something went wrong! \n\n @Funkaclau, fix me!",
        )
        print("oh shit")


def woodlandS(d, data, message, name):
    chance = randint(0, 99)
    print(chance)
    if chance <= 13:
        d["inv"].append("Dried Leaf")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Dried Leaf 🍁",
        )
        print("leaf")
    elif 14 <= chance <= 28:
        print("got Plain Wood")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found Wood 🪵",
        )
        d["inv"].append("Plain Wood")

    elif 29 <= chance <= 33:
        print("got Pinecone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Pinecone 🌲",
        )
        d["inv"].append("Pinecone")

    elif 34 <= chance <= 42:
        print("got Tree Bark")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Tree Bark 🌳",
        )
        d["inv"].append("Tree Bark")

    elif 43 <= chance <= 51:
        print("Orange")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Orange... 🍊",
        )
        d["inv"].append("Orange")
    elif 52 <= chance <= 65:
        print("Grass Tuft")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Grass Tuft 🌿",
        )
        d["inv"].append("Grass Tuft")

    elif 65 <= chance <= 69:
        print("Bone")
        bot.send_message(
            message.chat.id, "🎁\n\n@" + name + " collecto has found a Small Bone 🦴"
        )
        d["inv"].append("Small Bone")

    elif 70 <= chance <= 78:
        print("Excrement")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found an Excrement 💩",
        )
        d["inv"].append("Excrement")
    elif 79 <= chance <= 83:
        print("Fig")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Fig 🍐",
        )
        d["inv"].append("Fig")
    elif 84 <= chance <= 88:
        print("Wild Berries")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Wild Berries 🫐",
        )
        d["inv"].append("Wild Berries")
    elif 89 <= chance <= 93:
        print("Rag")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rag... 📃",
        )
        d["inv"].append("Rag")
    elif 94 <= chance <= 97:
        print("Nail")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rusty Nail... 🪡",
        )
        d["inv"].append("Rusty Nail")
    elif 98 <= chance <= 99:
        print("Needle")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rusty Needle... 🪡",
        )
        d["inv"].append("Rusty Needle")
    else:
        print("oh shit")
        bot.send_message(message.chat.id, "@Funkaclau, something is wrong..")


def forestS(d, data, message, name):
    chance = randint(0, 99)
    print(chance)
    if chance <= 12:
        d["inv"].append("Dried Leaf")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Dried Leaf 🍁",
        )
        print("leaf")

    elif 13 <= chance <= 26:
        print("got Plain Wood")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found Wood 🪵",
        )
        d["inv"].append("Plain Wood")

    elif 27 <= chance <= 30:
        print("got Pinecone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Pinecone 🌲",
        )
        d["inv"].append("Pinecone")
    elif 31 <= chance <= 39:
        print("got Tree Bark")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Tree Bark 🌳",
        )
        d["inv"].append("Tree Bark")

    elif 40 <= chance <= 48:
        print("Orange")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Orange... 🍊",
        )
        d["inv"].append("Orange")

    elif 49 <= chance <= 52:
        print("Bone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Small Bone 🦴",
        )
        d["inv"].append("Small Bone")
    elif 53 <= chance <= 61:
        print("Excrement")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found an Excrement 💩",
        )
        d["inv"].append("Excrement")
    elif 62 <= chance <= 67:
        print("Fig")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Fig 🍐",
        )
        d["inv"].append("Fig")
    elif 68 <= chance <= 73:
        print("Green Mushroom")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Green Mushroom... 🟢🍄",
        )
        d["inv"].append("Green Mushroom")
    elif 74 <= chance <= 79:
        print("Wild Berries")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found a Wild Berries 🫐",
        )
        d["inv"].append("Wild Berries")
    elif 80 <= chance <= 87:
        print("Rag")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rag... 📃",
        )
        d["inv"].append("Rag")
    elif 88 <= chance <= 89:
        print("Resin")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found Resin ... 🌲",
        )
        d["inv"].append("Resin")
    elif 90 <= chance <= 93:
        print("Bamboo")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found Bamboo... 🎋",
        )
        d["inv"].append("Bamboo")
    elif 94 <= chance <= 97:
        print("Nail")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rusty Nail... 🪡",
        )
        d["inv"].append("Rusty Nail")
    elif chance >= 98:
        print("Needle")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rusty Needle... 🪡",
        )
        d["inv"].append("Rusty Needle")
    else:
        print("oh shit")
        bot.send_message(message.chat.id, "@Funkaclau, please fix me!")


def rockyS(d, data, message, name):
    chance = randint(0, 99)
    print(chance)
    if chance <= 13:
        d["inv"].append("Granite Stone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Granite... 🪨",
        )
        print("Granite")
    elif 14 <= chance <= 22:
        print("got whitestone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Whitestone... 🪨",
        )
        d["inv"].append("Whitestone")

    elif 23 <= chance <= 31:
        print("got Small Bone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Small Bone ... 🦴",
        )
        d["inv"].append("Small Bone")

    elif 32 <= chance <= 41:
        print("got Excrement")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found an Excrement 💩",
        )
        d["inv"].append("Excrement")

    elif 42 <= chance <= 50:
        print("Egg")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Seagull Egg... 🥚",
        )
        d["inv"].append("Seagull Egg")

    elif 51 <= chance <= 55:

        print("Barb Fig")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Barbary Fig... 🫒",
        )
        d["inv"].append("Barbary Fig")
    elif 56 <= chance <= 64:
        print("Cactus")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Small Cactus... 🌵",
        )
        d["inv"].append("Small Cactus")

    elif 65 <= chance <= 78:
        print("Gravel")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Gravel... 🪨",
        )
        d["inv"].append("Gravel")
    elif 79 <= chance <= 81:
        print("Whetstone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Whetsone... 🪨",
        )
        d["inv"].append("Whetstone")
    elif 82 <= chance <= 85:
        print("Rag")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rag... 📃",
        )
        d["inv"].append("Rag")
    elif 86 <= chance <= 92:
        print("Big Stone")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Big Flat Stone... 🪨",
        )
        d["inv"].append("Big Flat Stone")
    elif 93 <= chance <= 94:
        print("Nail")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rusty Nail... 🪡",
        )
        d["inv"].append("Rusty Nail")
    elif chance == 95:
        print("Needle")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rusty Needle...",
        )
        d["inv"].append("Rusty Needle 🪡")
    elif 96 <= chance <= 99:
        print("Spike")
        bot.send_message(
            message.chat.id,
            "🎁\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Rusty Spike...",
        )
        d["inv"].append("Rusty Spike")
    else:
        print("oh shit")
        bot.send_message(message.chat.id, "@Funkaclau, fix me!")


def home(d, data, message, name):
    if d["location"] != "Home":
        data["homeC"] += 1
        homeC(data, message, name)
        beltHome(d, data, message, name)
    else:
        bot.send_message(
            message.chat.id,
            f"                ⚠️⚠️⚠️\n\n"
            f"@{name}, your Collector {d['number']} is already at Home!",
        )


def returnHome(d, data, message, name):
    d["distance"] -= 1
    if d["distance"] == 0:
        d["location"] = "Home"
        bot.send_message(
            message.chat.id,
            f"@{name}, your Collector {d['number']} arrived Home 🏘 to deliver:\n"
            f"{d['inv']}\n\n"
            f"@Funkaclau will send all this NFTs next Monday",
        )
        data["nftout"].append(d["inv"])
        d["inv"] = []
        save_to_userfile(data, name)
        with open("nftout.json", "a") as f:
            f.write(name + ", ")
        print(data)
    else:
        save_to_userfile(data, name)
        bot.send_message(
            message.chat.id,
            f"@{name}, your Collector {d['number']} is currently {d['distance']} moves away from Home 🏘",
        )


def dropsSearch(d, data, message, name):
    if d["location"] == "Plains":
        bot.send_message(
            message.chat.id,
            "🔎 SEARCH 🔎\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is Searching 🔎 at "
            + d["location"]
            + " terrain!",
        )

        plainS(d, data, message, name)
        plainS(d, data, message, name)
        save_to_userfile(data, name)

    elif d["location"] == "Woodland":
        bot.send_message(
            message.chat.id,
            "🔎 SEARCH 🔎\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is Searching 🔎 at "
            + d["location"]
            + "!",
        )
        woodlandS(d, data, message, name)
        woodlandS(d, data, message, name)
        save_to_userfile(data, name)
    elif d["location"] == "Forest":
        bot.send_message(
            message.chat.id,
            "🔎 SEARCH 🔎\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is Searching 🔎 at "
            + d["location"]
            + " terrain!",
        )
        forestS(d, data, message, name)
        forestS(d, data, message, name)
        save_to_userfile(data, name)
    elif d["location"] == "Rocky":
        bot.send_message(
            message.chat.id,
            "🔎 SEARCH 🔎\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is Searching 🔎 at "
            + d["location"]
            + " terrain!",
        )
        rockyS(d, data, message, name)
        rockyS(d, data, message, name)
        save_to_userfile(data, name)
    elif d["location"] == "Muddy":
        bot.send_message(
            message.chat.id,
            "🔎 SEARCH 🔎\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is Searching 🔎 at "
            + d["location"]
            + " terrain!",
        )
        # no loot func
        d["inv"].append("Red Clay")
        d["inv"].append("Red Clay")
        bot.send_message(
            message.chat.id,
            "🔎 SEARCH 🔎\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 🔎 2 Clay!",
        )

        save_to_userfile(data, name)
    elif d["location"] == "Lake":
        # no loot func
        bot.send_message(
            message.chat.id,
            "🔎 SEARCH 🔎\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is Searching at the "
            + d["location"]
            + "!",
        )
        d["inv"].append("Water")
        d["inv"].append("Water")
        bot.send_message(
            message.chat.id,
            "🔎 SEARCH 🔎\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 🔎 2 Water!",
        )

        save_to_userfile(data, name)
    elif d["location"] == "Beach":
        bot.send_message(
            message.chat.id,
            "🔎 SEARCH 🔎\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is Searching 🔎 at the "
            + d["location"]
            + "!",
        )
        beachE(d, data, message, name)
        beachE(d, data, message, name)
        save_to_userfile(data, name)

    else:
        print("shit")


# Add distance from home to collector data
def addDist(d, data, message, name):
    d["distance"] += 1
    print("add dist")
    if d["distance"] > 4:
        d["distance"] = 4
    belt(d, data, message, name)


def localCheckChop(d, data, message, name):
    if d["location"] != "Woodland" and d["location"] != "Forest":
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + ", Collector "
            + str(d["number"])
            + " is currently at"
            + d["location"]
            + "...\n\n Your collector can't use /chop at "
            + d["location"]
            + "!",
        )

    else:
        bot.send_message(
            message.chat.id,
            "🪓 CHOP 🪓\n\n@"
            + name
            + ", Collector "
            + str(d["number"])
            + " is currently at "
            + d["location"]
            + " and is getting ready to chop!\n✅",
        )
        data["chopC"] += 1
        chopC(data, message, name)
        beltChop(d, data, message, name)


def localCheckMine(d, data, message, name):
    if d["location"] != "Rocky":
        bot.send_message(
            message.chat.id,
            " ⛏ MINE ❌\n\n"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is currently at "
            + d["location"]
            + "...\n\n He can't use /mine at "
            + d["location"]
            + "!",
        )

    else:
        print("can search at home")
        bot.send_message(
            message.chat.id,
            " ⛏ MINE ⛏ \n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is currently at "
            + d["location"]
            + " and getting ready to mine!\n✅",
        )
        data["mineC"] += 1
        mineC(data, message, name)
        beltMine(d, data, message, name)


# check location for DropS
def drops(d, data, message, name):
    if d["location"] == "Plains":
        plainE(d, data, message, name)
        save_to_userfile(data, name)
    elif d["location"] == "Woodland":
        woodlandE(d, data, message, name)
        save_to_userfile(data, name)
    elif d["location"] == "Forest":
        forestE(d, data, message, name)
        save_to_userfile(data, name)
    elif d["location"] == "Rocky":
        rockyE(d, data, message, name)
        save_to_userfile(data, name)
    elif d["location"] == "Muddy":
        # no loot func
        d["inv"].append("Red Clay")
        bot.send_message(
            message.chat.id,
            "🚶 EXPLORE 🚶\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Red Clay!",
        )
        save_to_userfile(data, name)
    elif d["location"] == "Lake":
        # no loot func
        d["inv"].append("Water")
        bot.send_message(
            message.chat.id,
            "🚶 EXPLORE 🚶\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Water!",
        )
        save_to_userfile(data, name)
    elif d["location"] == "Beach":
        beachE(d, data, message, name)
        save_to_userfile(data, name)
    else:
        print("shit")


# And Roll location after
def locatRoll(d, data, message, name):
    chance = randint(0, 99)
    if chance <= 28:
        d["location"] = "Plains"
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " arrived at "
            + d["location"],
        )
        addDist(d, data, message, name)
    elif 29 <= chance <= 49:
        d["location"] = "Woodland"
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " arrived at "
            + d["location"],
        )
        addDist(d, data, message, name)
    elif 50 <= chance <= 68:
        d["location"] = "Rocky"
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " arrived at "
            + d["location"],
        )
        addDist(d, data, message, name)
    elif 69 <= chance <= 85:
        d["location"] = "Forest"
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " arrived at "
            + d["location"],
        )
        addDist(d, data, message, name)
    elif 86 <= chance <= 89:
        d["location"] = "Muddy"
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " arrived at "
            + d["location"],
        )
        addDist(d, data, message, name)
    elif 90 <= chance <= 95:
        d["location"] = "Beach"
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " arrived at "
            + d["location"],
        )
        addDist(d, data, message, name)
    elif chance >= 96:
        d["location"] = "Lake"
        bot.send_message(
            message.chat.id,
            "@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " arrived at "
            + d["location"],
        )
        addDist(d, data, message, name)


def localCheck(d, data, message, name):
    if d["location"] != "Home":
        data["searchC"] += 1
        searchC(data, message, name)
        beltSearch(d, data, message, name)

    else:
        print("cant search at home")
        bot.send_message(
            message.chat.id,
            "🔎=❌\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " is currently at "
            + d["location"]
            + "...\n\n Your collector can't use /search 🔎 at Home 🏘",
        )


def stashLevelCheck(data, message, name):
    missingText = (
        "🧐 @"
        + name
        + ", you are still missing some ingredients.\n\n STASH INFO\n\nStash Lvl: "
        + str(data["stash"]["stashlevel"])
        + "\nWood Missing: "
        + str(data["stash"]["stashmissing"]["woodmissing"])
        + "\nGranite Missing: "
        + str(data["stash"]["stashmissing"]["stonemissing"])
        + "\nClay Missing: "
        + str(data["stash"]["stashmissing"]["claymissing"])
        + "\n Nail Missing: "
        + str(data["stash"]["stashmissing"]["nailmissing"])
        + "\n\nCurrent Space: "
        + str(data["stash"]["stashspace"] - int(len(data["stash"]["stashinv"])))
        + "\nCurrent Stash Inventory: "
        + str(data["stash"]["stashinv"])
        + "\n\n End of report 🧐"
    )
    if data["stash"]["stashlevel"] <= 1:
        print("hello")
        if data["stash"]["stashmissing"]["woodmissing"] == 0:
            if data["stash"]["stashmissing"]["stonemissing"] == 0:
                stashLevel(data, message, name)
            else:
                bot.send_message(message.chat.id, missingText)

        elif data["stash"]["stashmissing"]["woodmissing"] > 0:
            bot.send_message(message.chat.id, missingText)
        elif data["stash"]["stashmissing"]["stonemissing"] > 0:
            bot.send_message(message.chat.id, missingText)

    elif data["stash"]["stashlevel"] > 1:
        if data["stash"]["stashmissing"]["woodmissing"] == 0:
            if data["stash"]["stashmissing"]["stonemissing"] == 0:
                if data["stash"]["stashmissing"]["claymissing"] == 0:
                    stashLevel(data, message, name)
                else:
                    bot.send_message(message.chat.id, missingText)
            else:
                bot.send_message(message.chat.id, missingText)
        else:
            bot.send_message(message.chat.id, missingText)


def stashLevel(data, message, name):
    if data["stash"]["stashlevel"] == 0:
        data["stash"]["stashlevel"] = 1
        data["stash"]["stashspace"] = 7
        data["stash"]["stashmissing"]["woodmissing"] = 5
        data["stash"]["stashmissing"]["stonemissing"] = 4
        save_to_userfile(data, name)
        bot.send_message(
            message.chat.id,
            "🎉📦 STASH 📦🎉\n@"
            + name
            + ",   Congratz!! \n\nYou just finished gathering all the ingredients to build your Stash Lvl 1.\n\n Now you can store 7 items inside your Stash! ",
        )
        with open("stash.json", "r") as f:
            fR = json.load(f)
            fR.append(name)
            fRJ = json.dumps(fR)
            with open("stash.json", "w") as f:
                f.write(fRJ)

    elif data["stash"]["stashlevel"] == 1:
        data["stash"]["stashlevel"] = 2
        data["stash"]["stashspace"] = 15
        data["stash"]["stashmissing"]["woodmissing"] = 4
        data["stash"]["stashmissing"]["claymissing"] = 5
        data["stash"]["stashmissing"]["stonemissing"] = 5
        save_to_userfile(data, name)
        bot.send_message(
            message.chat.id,
            "🎉📦 STASH 📦🎉\n@"
            + name
            + ",   Congratz!! \n\nYou just finished gathering all the ingredients to build your Stash Lvl 2.\n\n STASH INFO\n\nStash Lvl: "
            + str(data["stash"]["stashlevel"])
            + "\nWood Missing: "
            + str(data["stash"]["stashmissing"]["woodmissing"])
            + "\nGranite Missing: "
            + str(data["stash"]["stashmissing"]["stonemissing"])
            + "\nClay Missing: "
            + str(data["stash"]["stashmissing"]["claymissing"])
            + "\n\nCurrent Space: "
            + str(data["stash"]["stashspace"])
            + "\nCurrent Stash Inventory: "
            + str(data["stash"]["stashinv"])
            + "\n\n End of report 🧐",
        )

    elif data["stash"]["stashlevel"] == 2:
        data["stash"]["stashlevel"] = 3
        data["stash"]["stashspace"] = 24
        data["stash"]["stashmissing"]["claymissing"] = 2
        data["stash"]["stashmissing"]["stonemissing"] = 6
        data["stash"]["stashmissing"]["woodmissing"] = 7
        save_to_userfile(data, name)
        bot.send_message(
            message.chat.id,
            "🎉📦 STASH 📦🎉\n@"
            + name
            + ",   Congratz!! \n\nYou just finished gathering all the ingredients to build your Stash Lvl 3. \n\n STASH INFO\n\nStash Lvl: "
            + str(data["stash"]["stashlevel"])
            + "\nWood Missing: "
            + str(data["stash"]["stashmissing"]["woodmissing"])
            + "\nGranite Missing: "
            + str(data["stash"]["stashmissing"]["stonemissing"])
            + "\nClay Missing: "
            + str(data["stash"]["stashmissing"]["claymissing"])
            + "\n\nCurrent Space: "
            + str(data["stash"]["stashspace"])
            + "\nCurrent Stash Inventory: "
            + str(data["stash"]["stashinv"])
            + "\n\n End of report 🧐",
        )
    elif data["stash"]["stashlevel"] == 3:
        data["stash"]["stashlevel"] = 4
        data["stash"]["stashspace"] = 34

        save_to_userfile(data, name)
        bot.send_message(
            message.chat.id,
            "🎉📦 STASH 📦🎉\n@"
            + name
            + ",   Congratz!! \n\nYou just finished gathering all the ingredients to build your Stash Lvl 4.\n\n This is the current maximum level with a total of 34 Stash Space \n\n End of report 🧐",
        )


def eat(d, data, item, message, name):
    if item == "Wild Berries":
        d["inv"].remove(item)
        calories = 45
        data['foodBank'] += calories
        item = "Wild Berries 🫐"
        bot.send_message(
            message.chat.id,
            "🍽MEAL TIME🍽 \n\n@"
            + name
            + ", your Collector has successfully eaten "
            + str(item)
            + " and restored "
            + str(calories)
            + " Calories!",
        )
        save_to_userfile(data, name)

    elif item == "Orange":
        d["inv"].remove(item)
        item = "Orange 🍊"
        calories = 65
        data['foodBank'] += calories
        bot.send_message(
            message.chat.id,
            "🍽MEAL TIME🍽 \n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has successfully eaten "
            + str(item)
            + " and restored "
            + str(calories)
            + " Calories!",
        )
        save_to_userfile(data, name)

    elif item == "Fig":
        d["inv"].remove(item)
        calories = 35
        item = "Fig 🍐"
        data['foodBank'] += calories
        bot.send_message(
            message.chat.id,
            "🍽MEAL TIME🍽 \n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has successfully eaten "
            + str(item)
            + " and restored "
            + str(calories)
            + " Calories!",
        )
        save_to_userfile(data, name)

    elif item == "Barbary Fig":
        d["inv"].remove(item)
        calories = 60
        item = "Barbary Fig"
        data['foodBank'] += calories
        bot.send_message(
            message.chat.id,
            "🍽MEAL TIME🍽 \n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has successfully eaten "
            + str(item)
            + " and restored "
            + str(calories)
            + " Calories!",
        )
        save_to_userfile(data, name)
    elif item == "Friendship Cookie":
        d["inv"].remove(item)
        calories = 50
        data['foodBank'] += calories
        bot.send_message(
            message.chat.id,
            "🍽MEAL TIME🍽 \n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has successfully eaten "
            + str(item)
            + " and restored "
            + str(calories)
            + " Calories!",
        )
        save_to_userfile(data, name)


def checkFoodSupply(d, data, name, message, itemN):
    with open("market.json", "r") as f:
        marketData = json.load(f, cls=MarketDecoder)

        if itemN == 0:
            print(type(marketData))
            if marketData["food"]["Friendship Cookie"]["count"] > 0:
                print("passed")
                item = "Friendship Cookie"
                m = (
                    "🛒SHOPPING🛒\n\n @"
                    + name
                    + ", your Collector "
                    + str(d["number"])
                    + " has successfully bought "
                    + item
                    + " for 1 Coin! "
                )
                data["ccoins"] -= 1
                d["inv"].append(item)
                marketData["food"][item]["count"] -= 1
                marketData["coins"] += 1
                save_to_market(marketData)
                save_to_userfile(data, name)
                bot.send_message(message.chat.id, m)
        elif itemN == 1:
            if marketData["food"]["Wild Berries"]["count"] > 0:
                item = "Wild Berries"
                m = (
                    "🛒SHOPPING🛒\n\n @"
                    + name
                    + ", your Collector "
                    + str(d["number"])
                    + " has successfully bought "
                    + item
                    + " for 1 Coin! "
                )
                data["ccoins"] -= 1
                d["inv"].append(item)
                marketData["food"][item]["count"] -= 1
                marketData["coins"] += 1
                save_to_market(marketData)
                save_to_userfile(data, name)
                bot.send_message(message.chat.id, m)
        elif itemN == 2:
            if marketData["food"]["Barbary Fig"]["count"] > 0:
                item = "Barbary Fig"
                m = (
                    "🛒SHOPPING🛒\n\n @"
                    + name
                    + ", your Collector "
                    + str(d["number"])
                    + " has successfully bought "
                    + item
                    + " for 1 Coin! "
                )
                data["ccoins"] -= 1
                marketData["coins"] += 1
                marketData["food"][item]["count"] -= 1
                d["inv"].append(item)
                save_to_market(marketData)
                save_to_userfile(data, name)
                bot.send_message(message.chat.id, m)
        elif itemN == 3:
            if marketData["food"]["Orange"]["count"] > 0:
                item = "Orange"
                m = (
                    "🛒SHOPPING🛒\n\n @"
                    + name
                    + ", your Collector "
                    + str(d["number"])
                    + " has successfully bought "
                    + item
                    + " for 1 Coin! "
                )
                data["ccoins"] -= 1
                marketData["coins"] += 1
                marketData["food"][item]["count"] -= 1
                d["inv"].append(item)
                save_to_market(marketData)
                save_to_userfile(data, name)
                bot.send_message(message.chat.id, m)
        elif itemN == 4:
            if marketData["food"]["Fig"]["count"] > 0:
                item = "Fig"
                m = (
                    "🛒SHOPPING🛒\n\n @"
                    + name
                    + ", your Collector "
                    + str(d["number"])
                    + " has successfully bought "
                    + item
                    + " for 1 Coin! "
                )
                data["ccoins"] -= 1
                marketData["coins"] += 1
                marketData["food"][item]["count"] -= 1
                d["inv"].append(item)
                save_to_market(marketData)
                save_to_userfile(data, name)
                bot.send_message(message.chat.id, m)
        else:
            print(itemN)
            bot.send_message(
                message.chat.id,
                " It seems that what you are looking for is not available! \n\n ",
            )


def checkCoinSupply(d, data, name, message, itemN):
    with open("market.json", "r") as f:
        marketData = json.load(f, cls=MarketDecoder)
        print(itemN)
        if marketData["coins"] > 0:
            if itemN == 0:
                item = "Friendship Cookie"
                m = (
                    "💰🛒SHOPPING🛒💰\n\n @"
                    + name
                    + ", your Collector "
                    + str(d["number"])
                    + " has successfully Sold "
                    + item
                    + " for 1 Coin! "
                )
                data["ccoins"] += 1
                d["inv"].remove(item)
                marketData["food"][item]["count"] += 1
                marketData["coins"] -= 1
                save_to_market(marketData)
                save_to_userfile(data, name)
                bot.send_message(message.chat.id, m)
            elif itemN == 1:
                item = "Wild Berries"
                m = (
                    "💰🛒SHOPPING🛒💰\n\n @"
                    + name
                    + ", your Collector "
                    + str(d["number"])
                    + " has successfully Sold "
                    + item
                    + " for 1 Coin! "
                )
                data["ccoins"] += 1
                d["inv"].remove(item)
                marketData["food"][item]["count"] += 1
                marketData["coins"] -= 1
                save_to_market(marketData)
                save_to_userfile(data, name)
                bot.send_message(message.chat.id, m)
            elif itemN == 2:
                item = "Barbary Fig"
                m = (
                    "💰🛒SHOPPING🛒💰\n\n @"
                    + name
                    + ", your Collector "
                    + str(d["number"])
                    + " has successfully Sold "
                    + item
                    + " for 1 Coin! "
                )
                data["ccoins"] += 1
                d["inv"].remove(item)
                marketData["food"][item]["count"] += 1
                marketData["coins"] -= 1
                save_to_market(marketData)
                save_to_userfile(data, name)
                bot.send_message(message.chat.id, m)
            elif itemN == 3:
                item = "Orange"
                m = (
                    "💰🛒SHOPPING🛒💰\n\n @"
                    + name
                    + ", your Collector "
                    + str(d["number"])
                    + " has successfully Sold "
                    + item
                    + " for 1 Coin! "
                )
                data["ccoins"] += 1
                d["inv"].remove(item)
                marketData["food"][item]["count"] += 1
                marketData["coins"] -= 1
                save_to_market(marketData)
                save_to_userfile(data, name)
                bot.send_message(message.chat.id, m)
            elif itemN == 4:
                item = "Fig"
                m = (
                    "💰🛒SHOPPING🛒💰\n\n @"
                    + name
                    + ", your Collector "
                    + str(d["number"])
                    + " has successfully Sold "
                    + item
                    + " for 1 Coin! "
                )
                data["ccoins"] += 1
                d["inv"].remove(item)
                marketData["food"][item]["count"] += 1
                marketData["coins"] -= 1
                save_to_market(marketData)
                save_to_userfile(data, name)
                bot.send_message(message.chat.id, m)
            else:
                print("fuck")
        else:
            bot.send_message(
                message.chat.id,
                "❌🛒SHOPPING🛒❌\n@"
                + name
                + ", The Market doesnt seem to have Coins to purchase your item!\n\nIt has: "
                + str(marketData["coins"])
                + " Coins 💰!\n\nTry again later after someone has bought something from the market!",
            )


# Boots Checks
def boots(d, data, message, name):
    ## Boots Branch
    if d["gear"]["boots"]:
        data["foodBank"] -= 45
        print("- 45")
        cloverExplore(d, data, message, name)
        drops(d, data, message, name)

        ## No Boots Branch
    else:
        data["foodBank"] -= 50
        print("- 50")
        cloverExplore(d, data, message, name)
        drops(d, data, message, name)


def bootsHome(d, data, message, name):
    # Boots Branch
    if d["gear"]["boots"]:
        data['foodBank'] -= 45
        print("- 45")
        returnHome(d, data, message, name)
    # No Boots Branch
    else:
        data['foodBank'] -= 50
        print("- 50")
        # drops(d, data)
        returnHome(d, data, message, name)


def bootsSearch(d, data, message, name):
    # Boots Branch
    if d["gear"]["boots"]:
        data["foodBank"] -= 45
        print("- 45")
        cloverSearch(d, data, message, name)
        dropsSearch(d, data, message, name)

    # No Boots Branch
    else:
        data["foodBank"] -= 50
        print("- 50")
        # drops(d, data)
        cloverSearch(d, data, message, name)
        dropsSearch(d, data, message, name)
Footer
