#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The Ina Bot will be in charge of greeting new members, and role
assignment
Will be started by the controller"""


import sys
import os
import time
import json
import random
import discord
MY_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MY_PATH + '/../')

import cogo.controller #pylint: disable=C0413

CLIENT = cogo.controller.assign_client()
TOKEN = sys.argv[1]
SERVER_ID = "370170357488812032"
GREETING_ID = "406963397201100800"
ADMIN_ID = "408012712761622560"

SERVER = None
GREETING_CHANNEL = None
ADMIN_CHANNEL = None
DATA = None
CHANGE_PRESENCE_COUNTER = 20



@CLIENT.event
async def on_ready():
    """Event hook that triggers when bot is signed in"""
    global SERVER #pylint: disable=W0603
    SERVER = CLIENT.get_server(SERVER_ID)

    global GREETING_CHANNEL #pylint: disable=W0603
    GREETING_CHANNEL = SERVER.get_channel(GREETING_ID)

    global ADMIN_CHANNEL #pylint: disable=W0603
    ADMIN_CHANNEL = SERVER.get_channel(ADMIN_ID)

    with open('cogo/data/ina.json') as file:
        global DATA #pylint: disable=W0603
        DATA = json.load(file)

    await CLIENT.send_typing(ADMIN_CHANNEL)
    time.sleep(.2)
    await CLIENT.change_presence(game=discord.Game(name=DATA["data"]["games"][0]))
    await CLIENT.send_message(ADMIN_CHANNEL, "Ina just started.")

@CLIENT.event
async def on_typing(_, __, ___):
    """This hook is mostly used to count down the presence counter to change
    presence"""
    global CHANGE_PRESENCE_COUNTER #pylint: disable=W0603
    CHANGE_PRESENCE_COUNTER -= 1

    if CHANGE_PRESENCE_COUNTER <= 0:
        CHANGE_PRESENCE_COUNTER = 20
        await CLIENT.change_presence(game=discord.Game(name=DATA["data"]["games"][
            random.randint(0, len(DATA["data"]["games"]))]))
        await CLIENT.send_message(ADMIN_CHANNEL, "changed presence")





@CLIENT.event
async def on_member_join(member):
    """greets a member"""
    await CLIENT.send_typing(GREETING_CHANNEL)
    time.sleep(2)
    greetings = DATA["data"]["greetings"][random.randint(0, len(DATA["data"]["greetings"]))]
    await CLIENT.send_message(GREETING_CHANNEL, greetings.format(member.name))
    await CLIENT.send_message(ADMIN_CHANNEL, "{} joined".format(member.name))
    await CLIENT.send_message(member, "WTF IS THIS I NEED TO FILL THIS WITH USEFUL SHIT")





CLIENT.run(TOKEN)
