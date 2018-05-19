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

class Role():

    def __init__(self, name, id, server):
        self.name = name
        self.id = id
        server.roles = [self]

class Server():
    """mock server class"""
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.roles = None

    @staticmethod
    def get_channel(id):
        """mocks the get_channel function of the original class"""
        return Channel(name="TestChannel", id=id)

    def method_two(self):
        """method to satisfy linter"""
        pass

class Channel():
    """mock channel class"""
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def method_one(self):
        """method to satisfy linter"""
        pass
    def method_two(self):
        """method to satisfy linter"""
        pass

class Member():
    MemberList = []

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.role = []
        Member.Member = self

class Message():
    def __init__(self, author, content, channel):
        self.author = author
        self.content = content
        self.channel = channel

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
    def get_server(id):
        """mocks the get_server function of the original client"""
        server = Server(name="TestServer", id=id)
        return server

    async def send_message(self, chann, message):
        """mocks send_message function"""
        await asyncio.sleep(0)

    async def change_presence(self, game):
        """mocks send_message function"""
        await asyncio.sleep(0)

    async def add_roles(self, member, role):
        member.role.append(role)

    async def remove_roles(self, member, role):
        member.role.remove(role)

    def get_member(self, id):
        return Member.Member
