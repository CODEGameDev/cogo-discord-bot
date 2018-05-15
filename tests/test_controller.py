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

    assert results["britta"] != None
    #assert results["jonathan"] != None <-- commented out until implementation
    #assert results["luka"] != None     <-- commented out until implementation

def test_start_britta():
    """tests the startup_britta function of the controller"""
    process = cogo.controller.start_britta()

    assert process.poll() is None
    process.kill()

def test_assign_client_in_test_env():
    """tests the assign_client function of the controller while environment "test" is set"""
    assert isinstance(cogo.controller.assign_client(), tests.mock.discord.Client)

def test_assign_client_in_prod_env():
    """tests the assign_client function of the controller while environment "test" is not set"""
    del sys.called_from_test
    assert isinstance(cogo.controller.assign_client(), discord.Client)

    sys.called_from_test = True

def main():
    """runs all tests for coverage checking"""
    test_startup_routine()
    test_start_britta()




if __name__ == '__main__':
    main()
