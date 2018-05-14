#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test module.
test with ```$ pytest``` in project directory
```$ coverage test_sample.py``` should return 100% for all files!
should return 100%
"""

import sys
import os
MY_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MY_PATH + '/../')

import cogo.foobar #pylint: disable=C0413


def test_main():
    """tests placeholder method"""
    assert cogo.foobar.hello_word() == "world"


if __name__ == '__main__':
    test_main()
