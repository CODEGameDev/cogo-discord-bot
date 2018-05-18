#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""module supposed to mock the behaviour of the discord api for test purposes"""
import asyncio

class Game():
    """mock game class"""
    def __init__(self, name):
        self.name = name

    def method_one(self):
        """method to satisfy linter"""
        pass
    def method_two(self):
        """method to satisfy linter"""
        pass

class Server():
    """mock server class"""
    def __init__(self, name, _id):
        self.name = name
        self._id = id

    @staticmethod
    def get_channel(_id):
        """mocks the get_channel function of the original class"""
        return Channel(name="TestChannel", _id=_id)

    def method_two(self):
        """method to satisfy linter"""
        pass

class Channel():
    """mock channel class"""
    def __init__(self, name, _id):
        self.name = name
        self._id = id

    def method_one(self):
        """method to satisfy linter"""
        pass
    def method_two(self):
        """method to satisfy linter"""
        pass

class Loop():
    """mock loop class"""
    def __init__(self):
        pass

    def create_task(self, _):
        pass

class Client():
    """mock client class"""
    loop = Loop()


    def __init__(self):
        self.user = ""
        self.servers = ""

    @staticmethod
    def get_server(_id):
        """mocks the get_server function of the original client"""
        server = Server(name="TestServer", _id=_id)
        return server

    async def send_message(self, chann, message):
        """mocks send_message function"""
        await asyncio.sleep(0)

    async def change_presence(self, game):
        """mocks send_message function"""
        await asyncio.sleep(0)
