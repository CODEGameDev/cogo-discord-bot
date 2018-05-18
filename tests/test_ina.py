#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test module.
test with ```$ pytest``` in project directory
```$ coverage test_sample.py``` should return 100% for all files!
should return 100%
"""

import sys
import os
import discord
import pytest
import asyncio

MY_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MY_PATH + '/../')

from cogo.ina import InaBot #pylint: disable=C0413

SERVER = discord.Server(id=1, name="TestServer")
CHANNEL = discord.Channel(name="testing", server=SERVER)

def test_generate_channel_report_error():
    purpose = "testing"

    result = InaBot.generate_channel_found_report(purpose, None)
    assert result == "WARNING: Could not find testing channel!\n"

def test_generate_channel_report_success():
    purpose = "testing"
    channel = CHANNEL

    result = InaBot.generate_channel_found_report(purpose, channel)
    assert result == "Found testing channel: `testing`\n"

def test_generate_conn_report_error():
    with pytest.raises(ValueError, match="Bad ServerID"):
        InaBot.generate_connection_report(None)

def test_generate_conn_report_success():
    results = InaBot.generate_connection_report(SERVER)
    assert results == "Ina now online! Fully connected to TestServer.\n"

def test_generate_loop_report():
    results = InaBot.generate_loop_report("test_loop", 24)
    assert results == "Started test_loop loop\nRunning every 24 hours\n"

def test_hours_to_seconds():
    assert InaBot.hours_to_seconds(1) == 3600
    assert InaBot.hours_to_seconds(24.0) == 86400
    with pytest.raises(ValueError):
        InaBot.hours_to_seconds("bad_input")

def test_ina_bot_init():
    bot = InaBot(123)

    assert bot._server_id == 123 #pylint: disable=W0212
    assert bot.server is None
    assert bot.greetings_channel is None
    assert bot.logging_channel is None
    assert bot.assignment_channel is None
    assert bot.data is None
    assert bot.logging_buffer == ""

@pytest.mark.asyncio
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
async def test_on_ready():
    bot = InaBot(1)

    await bot.on_ready()

    assert bot.server is not None
    assert bot.logging_channel is not None
    assert bot.greetings_channel is not None
    assert bot.assignment_channel is not None

def test_start_loop():
    def functional_function(_):
        return 1+1
    bot = InaBot(1)
    assert bot.logging_buffer == ""
    bot.start_loop("name", functional_function, 1)
    assert bot.logging_buffer != ""

def test_load_json():
    bot = InaBot(1)

    assert bot.data is None
    bot.load_json()
    assert bot.data


@pytest.mark.asyncio
async def test_refresh_json_loop():
    bot = InaBot(1)

    assert bot.data is None
    await bot.refresh_json_loop(0)
    assert bot.data

@pytest.mark.asyncio
async def test_presence_loop():
    bot = InaBot(1)

    bot.load_json()
    await bot.presence_loop(0)

def test_get_instance_server():
    bot = InaBot(1)

    assert bot.server is None
    bot.get_instance_server()
    assert bot.server

def test_acquire_channel():
    bot = InaBot(1)

    assert bot.acquire_channel(None) is None
    bot.get_instance_server()
    assert bot.acquire_channel(1)

@pytest.mark.asyncio
async def test_report():
    bot = InaBot(1)

    await bot.report("formatless report")

@pytest.mark.asyncio
async def test_report_buffer():
    bot = InaBot(1)
    bot.logging_buffer = CHANNEL

    await bot.report_buffer()
    bot.logging_buffer = "HELLO WORLD"
    await bot.report_buffer()
    assert bot.logging_buffer == ""

@pytest.mark.asyncio
async def test_on_member_join():
    bot = InaBot(1)
    member = discord.Member(user={'name': "Steve", 'id': 1})
    bot.get_instance_server()
    bot.load_json()


    await bot.on_member_join(member)

@pytest.mark.asyncio
async def test_on_member_remove():
    bot = InaBot(1)
    member = discord.Member(user={'name': "Steve", 'id': 1})

    await bot.on_member_remove(member)


def test_generate_pm_welcome():
    bot = InaBot(1)
    bot.get_instance_server()
    bot.load_json()

    results = bot.generate_pm_welcome()
    expected_string = "Welcome to TestServer!"

    assert results == expected_string

@pytest.mark.asyncio
async def test_send_greeting_per_pm():
    bot = InaBot(1)
    bot.load_json()
    bot.get_instance_server()

    member = discord.Member(user={'name': "Steve", 'id': 1})

    await bot.send_greeting_per_pm(member)

@pytest.mark.asyncio
async def test_send_pm():
    bot = InaBot(1)
    message = "ROFL"

    member = discord.Member(user={'name': "Steve", 'id': 1})
    await bot.send_pm(member, message)

@pytest.mark.asyncio
async def test_send_greeting():
    bot = InaBot(1)
    bot.load_json()

    member = discord.Member(user={'name': "Steve", 'id': 1})
    await bot.send_greeting(member)
