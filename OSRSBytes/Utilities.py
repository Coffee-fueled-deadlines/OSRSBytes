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
__copyright__  = 'Copyright 2022, CFDeadlines'
__credits__    = ['CFDeadlines (Lead Programmer, Creator)']
__license__    = 'EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)'
__version__    = '1.1.0'
__maintainer__ = 'CFDeadlines'
__email__      = 'cookm0803@gmail.com'
__status__     = 'Open'

class Utilities(object):
	def __init__(self):
		self.getLocation()

	def getLocation(self):
		self.__package_dir__ = os.path.dirname(os.path.realpath(__file__))
		self.__here__ = self.__package_dir__
		self.__this__ = self.__here__
		self.__script__ = self.__this__		