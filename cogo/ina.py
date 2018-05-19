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
    def __init__(self, server_id):
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

    async def on_ready(self):
        """Startup Routine"""
        self.get_instance_server()

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

        self.start_loop("JSON", self.refresh_json_loop_wrapper, 24)
        self.start_loop("presence", self.presence_loop_wrapper, 12)

        await self.report_buffer()

    async def on_member_join(self, new_member):
        """Hook that gets called when a new member joins"""
        await self.report("New Member joined: {}".format(new_member.name))
        await self.send_greeting(new_member)
        await self.send_greeting_per_pm(new_member)

    async def on_member_remove(self, old_member):
        """Hook that gets called when a member leaves"""
        await self.report("Member left: {}".format(old_member.name))

    async def on_message(self, message):
        """Hook that gets called on new message"""
        if message.channel == self.assignment_channel and message.content.startswith("."):
            await self.interpret_command(message)

    def get_instance_server(self):
        """grabs the server and writes it to attributes"""
        self.server = self.get_server(self._server_id)
        self.logging_buffer += InaBot.generate_connection_report(self.server)

    def start_loop(self, name, task, time_in_hours):
        """Starts loop, accepts parameters:
                name=str // name is the purpose of the loop
                task=func // task is the to-be-looped function
                time_in_hours=int // repeat time in hours"""
        time_in_seconds = InaBot.hours_to_seconds(time_in_hours)

        BASE_CLASS().loop.create_task(task(time_in_seconds))
        self.logging_buffer += InaBot.generate_loop_report(name, time_in_hours)

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
        with open('./cogo/data/ina.json') as json_file:
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

    async def interpret_command(self, message):
        """interprets commands recieved by on_message"""
        if message.content.startswith(".addrole"):
            message_buffer = message.content.split(" ")
            if len(message_buffer) > 1:
                if self.valid_role(message_buffer[1]):
                    await self.add_role_to_user(message.author, message_buffer[1])
                else:
                    await self.send_message(self.assignment_channel,
                                            "{} not available!".format(message_buffer[1]))
            else:
                await self.send_message(self.assignment_channel, "Command too short!")

        if message.content.startswith(".removerole"):
            message_buffer = message.content.split(" ")
            if len(message_buffer) > 1:
                if self.valid_role(message_buffer[1]):
                    await self.remove_role_from_user(message.author, message_buffer[1])
                else:
                    await self.send_message(self.assignment_channel,
                                            "{} not available!".format(message_buffer[1]))
            else:
                await self.send_message(self.assignment_channel, "Command too short!")


    async def report(self, formatless_report_string):
        """Formatless report, to be used for error logging or rare occurances"""
        await self.send_message(self.logging_channel, formatless_report_string)

    async def report_buffer(self):
        """Formated report, to be used when logging routines"""
        await self.send_message(self.logging_channel, self.logging_buffer)
        self.logging_buffer = ""

    async def send_greeting(self, new_member):
        """Sends a random greeting message to the designated greeting channel"""
        rand_greeting = random.choice(self.data["data"]["greetings"])
        await self.send_message(self.greetings_channel, rand_greeting.format(new_member.name))

    async def send_greeting_per_pm(self, new_member):
        """Sends a detailed greeting via pm to a new member"""
        await self.send_pm(new_member, self.generate_pm_welcome())

    async def send_pm(self, member, message):
        """Sends a pm to a member"""
        await self.send_message(member, message)

    def valid_role(self, role):
        """checks if a role is valid"""
        return role in self.data["data"]["roles"]

    async def add_role_to_user(self, member, role_name):
        """adds a role to a member"""
        for role in self.server.roles:
            if role.name == role_name:
                break
        else:
            role = None

        await self.add_roles(member, role)

    async def remove_role_from_user(self, member, role_name):
        """removes a role from a user"""
        for role in self.server.roles:
            if role.name == role_name:
                break
        else:
            role = None

        await self.remove_roles(member, role)


    def generate_pm_welcome(self):
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
            return "Ina now online! Fully connected to {}.\n".format(server.name)
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
    BOT = InaBot(server_id=sys.argv[2])
    BOT.run(sys.argv[1])
