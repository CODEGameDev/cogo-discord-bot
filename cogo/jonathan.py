#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The Jonathan Bot will be in charge of greeting new members, and role
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

from discord.ext import commands

bot = commands.Bot(command_prefix='$')

class JonathanBot(BASE_CLASS):
    """docstring for JonathanBot. Will be started by the controller
    in test environments the class inherited here is a mock class"""

    def __init__(self, server_id):
        super(JonathanBot, self).__init__()
        self._server_id = server_id

        ###SERVER CONFIG###
        self.server = None
        self.logging_channel = None
        self.steam_key = None

        ###RUNTIME DATA###
        self.data = None
        self.logging_buffer = ""

    async def on_ready(self):
        """Startup Routine"""
        self.get_instance_server()
        self.steam_key = os.getenv("STEAM_API_KEY")

        self.logging_channel = self.server.get_channel(os.getenv("LOGGING_CHANNEL_ID"))
        self.logging_buffer += JonathanBot.generate_channel_found_report("logging",
                                                                    self.logging_channel)

        await self.report_buffer()

        self.start_loop("JSON", self.refresh_json_loop_wrapper, 24)
        self.start_loop("presence", self.presence_loop_wrapper, 12)

        await self.report_buffer()

    async def on_member_join(self, new_member):
        """Hook that gets called when a new member joins"""
        await self.report("New Member joined: {}".format(new_member.name))
        await self.send_question_per_pm(new_member)

    @bot.command()
    async def test(ctx, arg):
        await ctx.send(arg);

    def get_instance_server(self):
        """grabs the server and writes it to attributes"""
        self.server = self.get_server(self._server_id)
        self.logging_buffer += JonathanBot.generate_connection_report(self.server)

    def start_loop(self, name, task, time_in_hours):
        """Starts loop, accepts parameters:
                name=str // name is the purpose of the loop
                task=func // task is the to-be-looped function
                time_in_hours=int // repeat time in hours"""
        time_in_seconds = JonathanBot.hours_to_seconds(time_in_hours)

        BASE_CLASS().loop.create_task(task(time_in_seconds))
        self.logging_buffer += JonathanBot.generate_loop_report(name, time_in_hours)

    async def refresh_json_loop_wrapper(self, sleeptime):
        """wraps the loop, for test purposes"""
        while True:
            await self.refresh_json_loop(sleeptime)

    async def refresh_json_loop(self, sleeptime):
        """Loop for refreshing the self.data attribute according to sleeptime"""
        self.load_json()
        if self.data:
            await self.report("Successfully loaded/refreshed JSON.")
        else:
            await self.report("Error occured while loading JSON.")
        await asyncio.sleep(sleeptime)

    def load_json(self):
        """opens the specified json file and reads the data into self.data"""
        with open('./cogo/data/jonathan.json') as json_file:
            self.data = json.load(json_file)

    async def presence_loop_wrapper(self, sleeptime):
        """wraps the loop, for test purposes"""
        while True:
            await self.presence_loop(sleeptime)

    async def presence_loop(self, sleeptime):
        """Loop for refreshing the presence of the bot in discord, according to sleeptime"""
        game_list = self.data["data"]["games"]
        rand_game = random.choice(game_list)

        await self.change_presence(game=GAME_CLASS(name=rand_game))
        await asyncio.sleep(sleeptime)

    def acquire_channel(self, channel_id):
        """Getter of channels"""
        if channel_id:
            return self.server.get_channel(channel_id)

        return None

    async def report(self, formatless_report_string):
        """Formatless report, to be used for error logging or rare occurances"""
        await self.send_message(self.logging_channel, formatless_report_string)

    async def report_buffer(self):
        """Formated report, to be used when logging routines"""
        await self.send_message(self.logging_channel, self.logging_buffer)
        self.logging_buffer = ""

    async def send_question_per_pm(self, new_member):
        """Sends a detailed greeting via pm to a new member"""
        await self.send_pm(new_member, self.answer_pm_comparison())

    async def send_pm(self, member, message):
        """Sends a pm to a member"""
        await self.send_message(member, message)


    def answer_pm_comparison(self):
        """returns the formatted welcome message"""
        return self.data["data"]["pm_message"].format(self.server.name)


    @staticmethod
    def generate_channel_found_report(channel_purpose, channel_object):
        """Returns a string, formatted channel found report"""
        if channel_object:
            return "Found {} channel: `{}`\n".format(channel_purpose, channel_object.name)

        return "WARNING: Could not find {} channel!\n".format(channel_purpose)

    @staticmethod
    def generate_connection_report(server):
        """Returns a string, formatted connection report"""

        if server:
            return "Jonathan now online! Fully connected to {}.\n".format(server.name)
        else:
            raise ValueError("Bad ServerID")

    @staticmethod
    def generate_loop_report(loop_name, timer):
        """Returns a string, formatted loop report"""
        return "Started {} loop\nRunning every {} hours\n".format(loop_name, timer)

    @staticmethod
    def hours_to_seconds(hours):
        """Converst hours to seconds(int)"""
        return int(hours) * 60 * 60

if __name__ == '__main__':
    bot = JonathanBot(server_id=sys.argv[2])
    bot.run(sys.argv[1])
