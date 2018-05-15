#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to controll Discord client sessions. In the case that this is a test,
the controller will give out mock clients.
"""
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import discord

def startup_routine():
    """startup routine, fetches token and env"""
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path, verbose=True)
    test_flag = bool(hasattr(sys, 'called_from_test'))


    return {"test": test_flag,
            "britta": os.getenv("TOKEN_BRITTA"),
            "jonathan": os.getenv("TOKEN_JONATHAN"),
            "luka": os.getenv("TOKEN_LUKA")}
