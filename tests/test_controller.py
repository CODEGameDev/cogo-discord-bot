#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing the controller module"""

import sys
import os
MY_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MY_PATH + '/../')

import cogo.controller #pylint: disable=C0413


def test_startup_routine():
    """tests the startup_routine function of the controller"""
    results = cogo.controller.startup_routine()

    assert results["test"]
    assert results["britta"] != None
    #assert results["jonathan"] != None <-- commented out until implementation
    #assert results["luka"] != None     <-- commented out until implementation

def main():
    """runs all tests for coverage checking"""
    test_startup_routine()

if __name__ == '__main__':
    main()
