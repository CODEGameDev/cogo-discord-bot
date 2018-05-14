#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test module.
test with ```$ pytest``` in project directory
```$ coverage test_sample.py``` should return 100% for all files!
should return 100%
"""

import sys
import os
import cogo.foobar


MY_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MY_PATH + '/../')

def test_main():
    """tests placeholder method"""
    assert cogo.foobar.hello_word() == "world"
