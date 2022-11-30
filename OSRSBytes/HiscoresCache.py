#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
OSRSBytes() is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information.

EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)

HiscoresCache Module is responsible for allowing the user to directly modify the HiscoresCache after it has been created by the
Hiscores Module.  Note that this Module does not and cannot directly create the HiscoresCache files.  It wasn't created nor
intended to do that.
"""

"""
THIS IS DEPRECATED, DO NOT USE THIS
"""

# Generic/Built-in Imports
import os
import shelve
import time

# OSRSBytes Utilities package
from OSRSBytes.Utilities import Utilities

# META Data
__copyright__  = 'Copyright 2022, CFDeadlines'
__credits__    = ['CFDeadlines (Lead Programmer, Creator)']
__license__    = 'EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)'
__version__    = '1.3.0'
__maintainer__ = 'CFDeadlines'
__email__      = 'cookm0803@gmail.com'
__status__     = 'Deprecated'

################
#  Exceptions  #
################
class DoNotRunDirectly(Exception):
	pass

class CacheNotCreated(Exception):
	pass

class Deprecated(Exception):
	pass

############################
#  Do not run if __main__  #
############################
if __name__ == "__main__":
	raise DoNotRunDirectly("This library is not meant to be called as __main__, import it instead.")

###############################
# START: HiscoresCache Object #
###############################
class HiscoresCache(object):
	def __init__(self):
		raise Deprecated("Don't use this anymore")
