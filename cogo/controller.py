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
    returns dict with {test_env, TOKEN_INA, TOKEN_JONATHAN}"""
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path, verbose=True)


    return {"server_id": os.getenv("SERVER_ID"),
            "ina": os.getenv("TOKEN_INA"),
            "jonathan": os.getenv("TOKEN_JONATHAN")}


def new_process(file_name, token, server_id):
    """starts a new python process, used to start the bots"""
    return subprocess.Popen([sys.executable, file_name, token, server_id])

def start_ina(token=None, server_id=None):
    """starts the ina process. Own function for validation.
    if no token is provided, because the function is started externally,
    it retrieves token from environment"""

    if token is None:
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path, verbose=True)
        token = os.getenv("TOKEN_INA")

    if server_id is None:
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path, verbose=True)
        server_id = os.getenv("SERVER_ID")

    return new_process("cogo/ina.py", token, server_id)

def start_jonathan(token=None, server_id=None):
    """starts the jonathan process. Own function for validation.
    if no token is provided, because the function is started externally,
    it retrieves token from environment"""

    if token is None:
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path, verbose=True)
        token = os.getenv("TOKEN_JONATHAN")

    if server_id is None:
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path, verbose=True)
        server_id = os.getenv("SERVER_ID")

    return new_process("cogo/jonathan.py", token, server_id)



def assign_client():
    """Assigns a discord client, if executed in test it returns a mock
    client"""
    if hasattr(sys, 'called_from_test'):
        from tests.mock.discord import Client
        return Client

    return discord.Client

def assign_game_object():
    """Assigns a discord client, if executed in test it returns a mock
    client"""
    if hasattr(sys, 'called_from_test'):
        from tests.mock.discord import Game
        return Game

    return discord.Game

def main():
    """main function, called when script is main"""
    settings = startup_routine()
    ina = start_ina(settings["ina"], settings["server_id"])
    jonathan = start_jonathan(settings["jonathan"], settings["server_id"])

    return [ina]



if __name__ == '__main__':
    RUNNING_BOTS = main()

    # For the time being, the catch-all killer:
    for bot in RUNNING_BOTS:
        bot.terminate()
