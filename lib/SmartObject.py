#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Smart Object. "Bunch" pattern, may be something else.
"""

class SmartObject(dict):
    def __init__(self, *args, **kwds):
        super(SmartObject, self).__init__(*args, **kwds)
        self.__dict__ = self
        
