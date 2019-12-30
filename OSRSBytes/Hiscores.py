#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
OSRSBytes() is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information.

EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)

Hiscores Module is responsible for fetching and parsing player skill levels and scores from the OSRS API.
Changes that involve modifications to player based information should go in the Hiscores Module.

Note that this Module utilizes the secure.runescape.com api and is VERY slow sometimes.  I recommend using
a form of cacheing if you intend to utilize this in an application that'll serve multiple users checking for
updates frequently.
"""

# Generic/Built-in Imports
import http.client
import math
from sys import exit

# META Data
__author__     = 'Markis Cook'
__copyright__  = 'Copyright 2019, Markis H. Cook'
__credits__    = ['Markis Cook (Lead Programmer, Creator)']
__license__    = 'EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)'
__version__    = '1.1.0'
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
	def __init__(self, username: str, actype='N'):
		self.username = username
		self.accountType = actype.upper()
		self._getHTTPResponse()

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
		self.stats = subset

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
				return self.stats[skill.lower()][stype.lower()]
		except KeyError as KE:
			print("ERROR: skill {} does not exist".format(KE))
			exit(0)

	def error(self):
		print("Error occurred: {}".format(self.errorMsg))
		exit(0)
	##########################
	#  END: Hiscores Object  #
	##########################
