#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
OSRSBytes() is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information.

EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)

Utilies Module will contain methods and information that directly involve manipulation of this
package and returning information on it.  Currently, Location of Script is the only feature.

Usable with:
    print(Utilities().__package_dir__)
"""
import os

# META Data
__copyright__  = 'Copyright 2023, CFDeadlines'
__credits__    = ['CFDeadlines (Lead Programmer, Creator)', 'Riley Fitzgibbons (Contributor)']
__license__    = 'EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)'
__version__    = '1.3.2'
__maintainer__ = {
        'CFDeadlines': 'cookm0803@gmail.com',
        'Riley Fitz': "rileyfitzgibbons@gmail.com"
    }
__email__      = 'cookm0803@gmail.com'
__status__     = 'Open'

class Utilities(object):
    def __init__(self):
        self.getLocation()

    def getLocation(self):
        self.__package_dir__, self.__here__, self.__this__, self.__script__ = os.path.dirname(os.path.realpath(__file__))
