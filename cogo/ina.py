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

        ###SERVER CONFIG###
        self.server = None
        self.greetings_channel = None
        self.logging_channel = None
        self.assignment_channel = None

        ###RUNTIME DATA###
        self.data = None
        self.logging_buffer = ""

        self.run(token)

    async def on_ready(self):
        """Startup Routine"""
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

        self.start_loop("JSON", self.refresh_json_loop, 24)
        self.start_loop("presence", self.presence_loop, 12)

        await self.report_buffer()

    def start_loop(self, name, task, time_in_hours):
        """Starts loop, accepts parameters:
                name=str // name is the purpose of the loop
                task=func // task is the to-be-looped function
                time_in_hours=int // repeat time in hours"""
        time_in_seconds = InaBot.hours_to_seconds(time_in_hours)

        BASE_CLASS().loop.create_task(task(time_in_seconds))
        self.logging_buffer += InaBot.generate_loop_report(name, time_in_hours)

    async def refresh_json_loop(self, sleeptime):
        """Loop for refreshing the self.data attribute according to sleeptime"""
        while True:
            self.load_json()
            if self.data:
                await self.report("Successfully loaded/refreshed JSON.")
            else:
                await self.report("Error occured while loading JSON.")
            await asyncio.sleep(sleeptime)

    def load_json(self):
        """opens the specified json file and reads the data into self.data"""
        with open('./cogo/data/ina.json') as json_file:
            self.data = json.load(json_file)

    async def presence_loop(self, sleeptime):
        """Loop for refreshing the presence of the bot in discord, according to sleeptime"""
        while True:
            game_list = self.data["data"]["games"]
            rand_game = random.choice(game_list)

            await self.change_presence(game=GAME_CLASS(name=rand_game))
            await asyncio.sleep(sleeptime)

    def acquire_channel(self, channel_id):
        """Getter of channels"""
        if channel_id:
            return self.server.get_channel(channel_id)

        return None

    async def report(self, formatless_report_txt):
        """Formatless report, to be used for error logging or rare occurances"""
        await self.send_message(self.logging_channel, formatless_report_txt)

    async def report_buffer(self):
        """Formated report, to be used when logging routines"""
        await self.send_message(self.logging_channel, self.logging_buffer)
        self.logging_buffer = ""

    @classmethod
    def generate_channel_found_report(cls, channel_purpose, channel_object):
        """Returns a string, formatted channel found report"""
        if channel_object:
            return "Found {} channel: `{}`\n".format(channel_purpose, channel_object.name)

        return "WARNING: Could not find {} channel!\n".format(channel_purpose)

    @classmethod
    def generate_connection_report(cls, server):
        """Returns a string, formatted connection report"""

        if server:
            return "Ina now online! Fully connected to {}.\n".format(server.name)
        else:
            raise ValueError("Bad ServerID")

    @classmethod
    def generate_loop_report(cls, loop_name, timer):
        """Returns a string, formatted loop report"""
        return "Started {} loop\nRunning every {} hours\n".format(loop_name, timer)

    @classmethod
    def hours_to_seconds(cls, hours):
        """Converst hours to seconds(int)"""
        return hours * 60 * 60


InaBot(token=sys.argv[1],
       server_id=sys.argv[2])
