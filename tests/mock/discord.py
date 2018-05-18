#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""module supposed to mock the behaviour of the discord api for test purposes"""

class Client():
    """mock client class"""
    def __init__(self):
        self.user = ""
        self.servers = ""

    def method_one(self):
        """method to satisfy linter"""
        pass
    def method_two(self):
        """method to satisfy linter"""
        pass


class Game():
    """mock game class"""
    def __init__(self):
        self.name = ""

    def method_one(self):
        """method to satisfy linter"""
        pass
    def method_two(self):
        """method to satisfy linter"""
        pass
