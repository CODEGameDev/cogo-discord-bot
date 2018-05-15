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
# import discord

def startup_routine():
    """startup routine, fetches token and env.
    returns dict with {test_env, TOKEN_BRITTA, TOKEN_JONATHAN, TOKEN_INA}"""
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path, verbose=True)

    test_flag = bool(hasattr(sys, 'called_from_test'))


    return {"test": test_flag,
            "britta": os.getenv("TOKEN_BRITTA"),
            "jonathan": os.getenv("TOKEN_JONATHAN"),
            "ina": os.getenv("TOKEN_INA")}


def new_process(file_name, token):
    """starts a new python process, used to start the bots"""
    return subprocess.Popen(['python', file_name, token])

def start_britta(token):
    """starts the britta process. Own function for validation"""
    return new_process("britta.py", token)



def main():
    """main function, called when script is main"""
    settings = startup_routine()
    britta = start_britta(settings["britta"])



if __name__ == '__main__':
    main()
