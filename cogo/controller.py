#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to controll Discord client sessions. In the case that this is a test,
the controller will give out mock clients.
"""
import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import discord

def startup_routine():
    """startup routine, fetches token and env.
    returns dict with {test_env, TOKEN_BRITTA, TOKEN_JONATHAN, TOKEN_INA}"""
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path, verbose=True)


    return {"britta": os.getenv("TOKEN_BRITTA"),
            "jonathan": os.getenv("TOKEN_JONATHAN"),
            "ina": os.getenv("TOKEN_INA")}


def new_process(file_name, token):
    """starts a new python process, used to start the bots"""
    return subprocess.Popen([sys.executable, file_name, token])

def start_britta(token=None):
    """starts the britta process. Own function for validation.
    if no token is provided, because the function is started externally,
    it retrieves token from environment"""

    if token is None:
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path, verbose=True)
        token = os.getenv("TOKEN_BRITTA")

    return new_process("cogo/britta.py", token)



def assign_client():
    """Assigns a discord client, if executed in test it returns a mock
    client"""
    if hasattr(sys, 'called_from_test'):
        from tests.mock.discord import Client
        return Client()

    return discord.Client()


def main():
    """main function, called when script is main"""
    settings = startup_routine()
    britta = start_britta(settings["britta"])

    return [britta]



if __name__ == '__main__':
    RUNNING_BOTS = main()

    # For the time being, the catch-all killer:
    for bot in RUNNING_BOTS:
        bot.terminate()
