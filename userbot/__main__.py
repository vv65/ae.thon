#   BERLIN @UAETHON .

from userbot import bot
from sys import argv
import sys
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
import os
from telethon import TelegramClient
from var import Var
from userbot.utils import load_module
from userbot import LOAD_PLUG, BOTLOG_CHATID, LOGS
from pathlib import Path
import asyncio
import telethon.utils
import heroku3


async def add_bot():
    ((await bot.start()) if os.environ.get("PHONE") is None else (await bot.start(phone=os.environ.get("PHONE"))))
    bot.me = await bot.get_me() 
    bot.uid = telethon.utils.get_peer_id(bot.me)



if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    if Var.TG_BOT_USER_NAME_BF_HER is not None:
        print("Initiating Inline Bot")
        # ForTheGreatrerGood of beautification
        bot.tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=Var.APP_ID,
            api_hash=Var.API_HASH
        ).start(bot_token=Var.TG_BOT_TOKEN_BF_HER)
        print("Initialisation finished with no errors")
        print("Starting Userbot")
        bot.loop.run_until_complete(add_bot())
        if Var.HEROKU_APP_NAME and Var.HEROKU_API_KEY is not None:
            Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
            app = Heroku.app(Var.HEROKU_APP_NAME)
            heroku_var = app.config()
            variable = "SUDO_USERS"
            if variable in heroku_var:
                del heroku_var[variable]
            else:
                print("All Good!")
        print("Startup Completed")
    else:
        ((bot.start()) if os.environ.get("PHONE") is None else (bot.start(phone=os.environ.get("PHONE"))))
    

import glob
path = 'userbot/plugins/*.py'
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))

import userbot._core

print("Thank you for using Telethon UAE. Now the bot is working. Follow our channel : T.me/UAETHON")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
