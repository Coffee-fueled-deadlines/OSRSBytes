#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
OSRSBytes() is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information.

EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)

HiscoresCache Module is responsible for allowing the user to directly modify the HiscoresCache after it has been created by the
Hiscores Module.  Note that this Module does not and cannot directly create the HiscoresCache files.  It wasn't created nor
intended to do that.
"""

# Generic/Built-in Imports
import os
import shelve
import time

# OSRSBytes Utilities package
from OSRSBytes.Utilities import Utilities

# META Data
__author__     = 'Markis Cook'
__copyright__  = 'Copyright 2019, Markis H. Cook'
__credits__    = ['Markis Cook (Lead Programmer, Creator)']
__license__    = 'EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)'
__version__    = '1.2.0'
__maintainer__ = 'Markis Cook'
__email__      = 'cookm0803@gmail.com'
__status__     = 'Open'

################
#  Exceptions  #
################
class DoNotRunDirectly(Exception):
	pass

class CacheNotCreated(Exception):
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
		self.HiscoresCacheFilePath = Utilities().__package_dir__ + "\cache\hiscores.shelve"
		print(self.HiscoresCacheFilePath)
		if not os.path.exists(self.HiscoresCacheFilePath + ".dat"):
			raise CacheNotCreated("Cache has not yet been created.  Cache is created by the Hiscores library with caching enabled.")

	def destroyCache(self):
		"""destroyCache Method

		The destroyCache method completely destroys the HiscoresCache files including the directory in which
		these files are located.

		This is not reversible.
		"""
		try:
			os.remove( self.HiscoresCacheFilePath + ".dat" )
			os.remove( self.HiscoresCacheFilePath + ".bak" )
			os.remove( self.HiscoresCacheFilePath + ".dir" )

		except Exception as e:
			raise Exception(e)

		finally:
			os.rmdir( Utilities().__package_dir__ + "/cache/" )

	def clearExpiredCacheEntries(self):
		"""clearExpiredCacheEntries Method

		The clearExpiredCacheEntries method checks the HiscoresCache entries to see if any cache_ttl have reached
		their expiration time and then removes that user from the cache.

		After calling this method, one can utilize the self.usersDeleted and self.purgeCounter properties to check
		the number of users removed as well as the users removed.  Calling this method again clears both of those
		properties.
		"""
		try:
			HiscoresCache = shelve.open(self.HiscoresCacheFilePath)
			self.purgeCounter = 0
			self.usersDeleted = []
			for username in HiscoresCache:
				if HiscoresCache[username]['cache_ttl'] <= time.time():
					del HiscoresCache[username]
					self.usersDeleted.append(username)
					self.purgeCounter += 1
			return True
		except Exception as e:
			raise Exception(e)

		finally:
			HiscoresCache.close()

	def removeFromCache(self, username: str):
		"""removeFromCache Method

		The removeFromCache method allows for manual removal from cache by supplying the username of the individual to
		be removed.  If the individual isn't in the HiscoresCache file, this method returns None.  If the user has been
		removed from the HiscoresCache file, this method returns True.
		"""
		try: 
			HiscoresCache = shelve.open(self.HiscoresCacheFilePath)
			if username.lower() not in HiscoresCache:
				return None
			else:
				del HiscoresCache[username.lower()]
				return True
		except Exception as e:
			raise Exception(e)
		finally:
			HiscoresCache.close()
