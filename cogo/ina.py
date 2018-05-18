#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The Ina Bot will be in charge of greeting new members, and role
assignment
Will be started by the controller"""


import sys
import os
import json
import random
import asyncio
MY_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MY_PATH + '/../')

import cogo.controller #pylint: disable=C0413

BASE_CLASS = cogo.controller.assign_client()
GAME_CLASS = cogo.controller.assign_game_object()

class InaBot(BASE_CLASS):
    """docstring for InaBot. Will be started by the controller
    in test environments the class inherited here is a mock class"""

    def __init__(self, token, server_id):
        super(InaBot, self).__init__()
        self._server_id = server_id

        self.logging_buffer = ""

        self.server = None
        self.greetings_channel = None
        self.logging_channel = None
        self.assignment_channel = None

        self.data = None


        self.run(token)

    async def on_ready(self):
        self.server = self.get_server(self._server_id)
        self.logging_buffer += InaBot.generate_connection_report(self.server)

        self.logging_channel = self.server.get_channel(os.getenv("LOGGING_CHANNEL_ID"))
        self.logging_buffer += InaBot.generate_channel_found_report("logging",
                                                                    self.logging_channel)

        self.greetings_channel = self.server.get_channel(os.getenv("GREETING_CHANNEL_ID"))
        self.logging_buffer += InaBot.generate_channel_found_report("greetings",
                                                                    self.greetings_channel)


        self.assignment_channel = self.server.get_channel(None)
        self.logging_buffer += InaBot.generate_channel_found_report("role assignment",
                                                                    self.assignment_channel)

        await self.report_buffer()

        refresh_loop_timer = InaBot.hours_to_seconds(24)
        BASE_CLASS().loop.create_task(self.refresh_json_loop(refresh_loop_timer))
        self.logging_buffer += InaBot.generate_loop_report("JSON", refresh_loop_timer)

        game_change_timer = InaBot.hours_to_seconds(12)
        BASE_CLASS().loop.create_task(self.presence_loop(game_change_timer))
        self.logging_buffer += InaBot.generate_loop_report("presence", game_change_timer)



        await self.report_buffer()

    async def refresh_json_loop(self, sleeptime):
        while True:
            self.load_json()
            if self.data:
                await self.report("Successfully loaded/refreshed JSON.")
            else:
                await self.report("Error occured while loading JSON.")
            await asyncio.sleep(sleeptime)

    async def presence_loop(self, sleeptime):
        while True:
            game_list = self.data["data"]["games"]
            rand_game = random.choice(game_list)

            await self.change_presence(game=GAME_CLASS(name=rand_game))
            await asyncio.sleep(sleeptime)

    def acquire_channel(self, channel_id):
        if channel_id:
            return self.server.get_channel(channel_id)

        return None

    def load_json(self):
        #path = os.sys.argv[3]

        #if path is None:
        #    return

        with open('./cogo/data/ina.json') as json_file:
            self.data = json.load(json_file)

    async def report(self, formatless_report_txt):
        await self.send_message(self.logging_channel, formatless_report_txt)

    async def report_buffer(self):
        await self.send_message(self.logging_channel, self.logging_buffer)
        self.logging_buffer = ""

    @classmethod
    def generate_channel_found_report(cls, channel_purpose, channel_object):
        if channel_object:
            return "Found {} channel: `{}`\n".format(channel_purpose, channel_object.name)

        return "WARNING: Could not find {} channel!\n".format(channel_purpose)

    @classmethod
    def generate_connection_report(cls, server):
        if server:
            return "Ina now online! Fully connected to {}.\n".format(server.name)
        else:
            raise ValueError("Bad ServerID")

    @classmethod
    def generate_loop_report(cls, loop_name, timer):
        return "Started {} loop\nRunning every {} seconds\n".format(loop_name, timer)

    @classmethod
    def hours_to_seconds(cls, hours):
        return hours * 60 * 60


InaBot(token=sys.argv[1],
       server_id=sys.argv[2])
