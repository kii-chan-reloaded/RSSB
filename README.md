# RSSB
Reddit Secret Santa Bot

## Overview
This is a Reddit bot that allows for "pseudo-anonymous" messaging to aid in a "Secret Santa"-style gift exchange. The bot will check its inbox at an interval you define on setup. When it receives a message, it will copy the message verbatim and send it to the designated recipient. The bot uses the PM title in conjunction with a list of Redditors to determine who to send a message to, and it will also provide links for pre-formatted PMs in every PM it sends. If a user receives a message from the bot, they do not need to use the links and can instead simply reply to the bot and the message will be forwarded. 

### Reporting and a Note on Security
To discourage offensive behavior through this bot, each message is saved to the local disk. If a user feels threatened or offended, each message can be reported to the moderators of the sub. The moderators will receive a copy of the message along with the usernames of both users involved and a <1000 character reason for reporting from the user who reported. A pre-formatted link is provided at the end of each message that allows the user to easily report any message they receive.

This does raise legitimate privacy and security issues for the users of this bot, as it falls on the bot maintainer to not only protect this information, but also respect it and delete it when appropriate. This, however, is the nature of the beast for these kind of events. It is recommended to run this bot on a computer/server behind a firewall, on a system with only local SSH capabilities at most to minimize the risk of information being obtained by nefarious methods. Furthermore, it is suggested to set the bot up with a very strong password, since Reddit doesn't allow for sent messages to be deleted. It would be best practice to inform your userbase to be mindful of the information they send through this bot (and the internet in general).

## Usage and Setup
Before anything, the usernames of Redditors participating in the event must be collected. It is left to you to decide how best to do that. Once a finalized list has been determined, Redditors must be assigned a Secret Santa through `santaList.csv`. A template has been provided, but the structure of the file is as follows:

|user|santa|
|---|---|
|Redditor 1|Redditor 2|
|Redditor 2|Redditor 3|
|Redditor 3|Redditor 1|

*In this example, Redditor 2 will be buying a gift for Redditor 1 and will be receiving a gift from Redditor 3.*

This file will be read by the bot on first boot and be used henceforth. If you need to change how the users are assigned, stop the bot and either delete `Objects/santaList.pkl`, or run it with the `--force` argument.

### Requirements
* Python 3.5+
 * Python Standard Library
* PRAW 5+

### Configuration
Before the bot will work, you will need to edit `Modules/secret.py`. The file contains instructions on how to do that and what information is needed.

### Running the Bot
The bot is designed with two modes in mind: running continuously on a server using a program like `screen`, or by executing it at predefined intervals using a program like `cron`. Both modes operate identically, and they are toggled through the `sleepTime` variable in `Modules/secret.py`.

When you start the bot, it will print markdown links for messaging a gift-giver and a gift-recipient. Because of how the bot works, these links are universal and work for everyone involved in the exchange, so these can be posted on the sidebar or a stickied post. Note that these links are also provided by the bot on every message it sends, so users do not need to come back to the thread/sidebar for every message they send.

## TODO

Future releases of this bot will likely have in-reddit functions available through PMs. Possible functions might include:

* Moderators to add/remove/reassign users in the exchange
* Moderators to reshuffle the exchange assignments
* More when the ideas come to me