#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing the controller module"""

import sys
import os
import discord
MY_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MY_PATH + '/../')

import cogo.controller #pylint: disable=C0413
import tests.mock.discord #pylint: disable=C0413

def test_startup_routine():
    """tests the startup_routine function of the controller"""
    results = cogo.controller.startup_routine()

    assert results["ina"] != None
    #assert results["jonathan"] != None <-- commented out until implementation
    #assert results["luka"] != None     <-- commented out until implementation

def test_start_ina():
    """tests the startup_ina function of the controller"""
    process = cogo.controller.start_ina()

    assert process.poll() is None
    process.kill()

def test_assign_client_in_test_env():
    """tests the assign_client function of the controller while environment "test" is set"""
    assert cogo.controller.assign_client() == tests.mock.discord.Client

def test_assign_client_in_prod_env():
    """tests the assign_client function of the controller while environment "test" is not set"""
    del sys.called_from_test
    client = cogo.controller.assign_client()
    assert client == discord.Client

    sys.called_from_test = True

def test_assign_game_in_test_env():
    """tests the assign_client function of the controller while environment "test" is set"""
    assert cogo.controller.assign_game_object() == tests.mock.discord.Game

def test_assign_game_in_prod_env():
    """tests the assign_client function of the controller while environment "test" is not set"""
    del sys.called_from_test
    game_object = cogo.controller.assign_game_object()
    assert game_object == discord.Game

    sys.called_from_test = True

def main():
    """runs all tests for coverage checking"""
    sys.called_from_test = True
    test_startup_routine()
    test_start_ina()
    test_assign_client_in_prod_env()
    test_assign_client_in_test_env()
    test_assign_game_in_prod_env()
    test_assign_game_in_test_env()
    del sys.called_from_test




if __name__ == '__main__':
    main()
