#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
OSRSBytes() is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information.

EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)

Hiscores Module is responsible for fetching and parsing player skill levels and scores from the OSRS API.
Changes that involve modifications to player based information should go in the Hiscores Module.

Note: This Module utilizes the secure.runescape.com api and response time is VERY slow sometimes.  I recommend using
the OSRSBytes' built in caching method (check the ReadMe on Github) or homebrew your own caching method into whatever
script you're creating.  It's possible that repetetive, rapid calls to the API with the same username may result in
throttling or IP Banning the script that's making these API Calls.  Caching is highly recommended regardless.
"""

# Generic/Built-in Imports
import http.client
import math
import os
from sys import exit
import shelve
import time

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

############################
#  Do not run if __main__  #
############################
if __name__ == "__main__":
	raise DoNotRunDirectly("This library is not meant to be called as __main__, import it instead.")

############################
#  START: Hiscores Object  #
############################
class Hiscores(object):
	"""Hiscores class
	
	The Hiscores class deals with collecting the required
	information needed to fetch user information from in-game
	API.  After being supplied necessary information, Hiscores
	class then sets self.stats dictionary with user information.
	
	Note that Methods prefixed by an underscore (_) would prefer that you stay out of their
	living room.  This means that we'd prefer you don't call them directly and instead let the
	class do it's job with them.  However, we're all consenting adults here, so if you need to
	call them, go ahead I guess.

	Args:
		self,
		username str: The username of the account that you
			      want to look up information on.
		actype   str: The account type of the account that
		              you want to lookup.  If not supplied
			      this argument defaults to 'N' Normal.
			      
	Returns:
		This object returns nothing.  Instead it sets the 
		value of self.stats with a dictionary of values
		keyed by the skill type. Example: self.stats['attack']
		
	Example Invocation:
		from OSRS-Hiscores import Hiscores
		account = Hiscores('Zezima', 'N')
		print(account.stats['attack']['level']) # displays attack level
	"""
	def __init__(self, username: str, actype='N', caching: bool=False, cacheTTL: int=3600, force_cache_update: bool=False):
		self.username = username.lower()
		self.accountType = actype.upper()

		# Set caching variable
		self.caching = caching

		# Store TTL for Cache in seconds
		self.cacheTTL = cacheTTL

		# Check if caching
		if self.caching and not force_cache_update:
			# Check if cache needs to be updated
			if self._checkCache():
				# Cache is expired, continue with Connection
				self._getHTTPResponse()
			else:
				self._fetchCacheAndSetStats()
		elif self.caching and force_cache_update:
			self._getHTTPResponse()
		else:
			# Caching disabled, continue with Connection
			self._getHTTPResponse()
		
	def _checkCache(self):
		"""_checkCache Method

		The _checkCache method is used by the class to determine whether or not the HiscoresCache needs to be
		updated for the user specified in object initialization.  On returning True, cache is updated.  On 
		returning False, cache is not updated.
		"""
		if os.path.exists( Utilities().__package_dir__ + "/cache/hiscores.shelve.dat" ):
			tempSkills = shelve.open( Utilities().__package_dir__ + "/cache/hiscores.shelve" )
			try:
				tempSkills[self.username]
				if tempSkills[self.username]['cache_ttl'] > time.time():
					# If cache_ttl is greater than current timestamp, cache is still valid
					return False
				else:
					# If cache_ttl is less than or equal to current timestamp, cache is expired
					return True

			except KeyError:
				# Username is not present in cache, user needs to be cached
				return True

			finally:
				# Close the shelve
				tempSkills.close()

		# If cache hasn't been built yet, cache needs to be updated
		return True

	def _cacheData(self):
		"""_cacheData Method

		The _cacheData method is used by the class to create/update the cache with the Hiscores information
		retrieved on the specific user.  Cache is stored by username in one file.  This means that the HiscoresCache
		file will contain Cache on ALL users queried ever.
		"""
		if not os.path.exists( Utilities().__package_dir__ + "/cache/"):
			os.mkdir( Utilities().__package_dir__ + "/cache/")
		try:
			HiscoresCache = shelve.open( Utilities().__package_dir__ + "/cache/hiscores.shelve" )
			HiscoresCache.update(self.stats)

		except Exception as e:
			raise Exception(e)

		finally:
			HiscoresCache.close()

	def _fetchCacheAndSetStats(self):
		try:
			HiscoresCache = shelve.open( Utilities().__package_dir__ + "/cache/hiscores.shelve" )
			self.stats = dict(HiscoresCache)

		except Exception as e:
			raise Exception(e)

		finally:
			HiscoresCache.close()

	def getCacheTTLRemaining(self):
		try:
			HiscoresCache = shelve.open( Utilities().__package_dir__ + "/cache/hiscores.shelve" )
			return math.ceil(HiscoresCache[self.username]['cache_ttl'] - time.time())
		except Exception as e:
			return Exception(e)
		finally:
			HiscoresCache.close()

	def _getHTTPResponse(self):
		"""getHTTPResponse() method
		
		The getHTTPResponse() method communicates with the OSRS Hiscores API
		and supplies the required information from self.username and
		self.actype to pull the given users stats and hiscore information.
		
		Args:
			self
			
		Returns:
			None
			
		Triggers:
			self.processResponse(): This method is always triggered, regardless
			                        of whether or not the query to the API returned
						successfully or not.
		"""
		conn = http.client.HTTPSConnection('secure.runescape.com')
		if self.accountType == 'N':
			conn.request("GET", "/m=hiscore_oldschool/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == 'IM':
			conn.request("GET", "/m=hiscore_oldschool_ironman/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == "UIM":
			conn.request("GET", "/m=hiscore_oldschool_ultimate/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == "HIM":
			conn.request("GET", "/m=hiscore_oldschool_hardcore_ironman/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		self._processResponse()

	def _processResponse(self):
		"""processResponse() method
		
		The processResponse() method processes the response received during the
		getHTTPResponse() method.  It handles potential 404 errors, 403 errors
		and the like and sets self.errorMsg accordingly.  On successful Response
		data is stored in self.data and sent to the self.parseData() method.
		
		Args:
			self
			
		Returns:
			None
			
		Triggers:
			self.error(): This method is triggered whenever the self.status of
			              a request is not 200 (failed).
				      
			self.parseData(): This method is called when self.status is 200 (success)
		"""
		if self.status != 200:
			self.errorMsg = "Player name given not found in account type provided.  Valid account types are, 'N' (Normal), 'IM' (Iron Man), 'UIM' (Ultimate Iron Man), 'HIC' (Hardcore Iron Man)"
			self.error()
		else:
			self.data = self.response.read().decode('ascii')
			self._parseData()

	def _parseData(self):
		"""parseData() method
		
		The parseData() method parses the self.data processed in the processResponse()
		method.  Data parsed in placed in the self.stats dictionary.
		
		Args:
			self
			
		Returns:
			None
			
		Triggers:
			None
		"""
		self.data = self.data.replace('\n',',')
		self.data = self.data.split(',')
		subset = {}

		# Totals
		info = {}
		info['rank']       = self.data[0]
		info['level']      = self.data[1]
		info['experience'] = self.data[2]
		subset['total']    = info

		skills = [
			  	'attack',
		          'defense',
		          'strength',
		          'hitpoints',
		          'ranged',
		          'prayer',
		          'magic',
		          'cooking',
		          'woodcutting',
		          'fletching',
		          'fishing',
		          'firemaking',
		          'crafting',
		          'smithing',
		          'mining',
		          'herblore',
		          'agility',
		          'thieving',
		          'slayer',
		          'farming',
		          'runecrafting',
		          'hunter',
		          'construction'
		           ]
		counter = 0
		for i in range(len(skills)):
			info = {}
			info['rank']       = int(self.data[counter+3])
			info['level']      = int(self.data[counter+4])
			info['experience'] = int(self.data[counter+5])
			level = int(info['level']+1)
			info['next_level_exp'] = math.floor(sum((math.floor(level + 300 * (2 ** (level / 7.0))) for level in range(1, level)))/4)
			info['exp_to_next_level'] = int(info['next_level_exp'] - info['experience'])
			subset[skills[i]] = info
			counter += 3

		# set stats dictionary
		self.stats = {}
		self.stats[self.username] = subset
		self.stats[self.username]['cache_ttl'] = time.time() + self.cacheTTL
		
		# Check for caching
		if self.caching:
			self._cacheData()


	def skill(self, skill, stype: str = 'level'):
		"""skill() method
		
		The skill() method is a more dynamic, intuitive way to access stats
		then the self.stats dictionary variable.  It allows for a user to
		provide the skill and stype (level, rank, experience) of the skill
		they wish information on.
		
		Args:
			skill (str): The OSRS skill to get information on
			
			stype (str): One of 'level', 'rank', or 'experience'
			             to receive information for.  If not
				     supplied, stype is assumed to be
				     'level'
		Returns:
			self.stats[skill][stype] (int): The info you requested
		
		"""
		try:
			if stype.lower() not in ['rank','level','experience','exp_to_next_level']:
				print("stype must be 'rank','level', or experience'")
				exit(0)
			else:
				return self.stats[self.username][skill.lower()][stype.lower()]
		except KeyError as KE:
			print("ERROR: skill {} does not exist".format(KE))
			exit(0)

	def error(self):
		print("Error occurred: {}".format(self.errorMsg))
		exit(0)
	##########################
	#  END: Hiscores Object  #
	##########################
