#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Configuration of pytest"""
import sys

def pytest_configure(*_):
    """adds a system flag for mocking"""
    sys.called_from_test = True

def pytest_unconfigure(*_):
    """deletes system flag"""
    del sys.called_from_test
