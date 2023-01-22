#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
OSRSBytes() is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information.

EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)
"""

# Initialize OSRSBytes Modules
from OSRSBytes.Hiscores import *
from OSRSBytes.HiscoresCache import *
from OSRSBytes.Items import *
from OSRSBytes.Utilities import *

# META Data
__copyright__  = 'Copyright 2022, CFDeadlines'
__credits__    = ['CFDeadlines (Lead Programmer, Creator)', 'Riley Fitzgibbons (Contributor)']
__license__    = 'EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)'
__version__    = '1.3.0'
__maintainer__ = {
        'CFDeadlines': 'cookm0803@gmail.com',
        'Riley Fitz': "rileyfitzgibbons@gmail.com"
    }
__email__      = 'cookm0803@gmail.com'
__status__     = 'Open'

################
#  Exceptions  #
################
class DoNotRunDirectly(Exception):
    pass

############################
#  Do not run if __main__  #
############################
if __name__ == "__main__":
    raise DoNotRunDirectly("This library is not meant to be called as __main__, import it instead.")

