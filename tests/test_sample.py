#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import cogo.foobar

def func():
    return "hello"

def test_answer():
    assert func() == "hello"

def test_main():
    assert cogo.foobar.hello_word() == "world"
