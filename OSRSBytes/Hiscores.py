#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
OSRSBytes() is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information.

EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)

Hiscores Module is responsible for fetching and parsing player skill levels and scores from the OSRS API.
Changes that involve modifications to player based information should go in the Hiscores Module.
"""

# Generic/Built-in Imports
import http.client
import math
import os
import time

from OSRSBytes.Utilities import Utilities

# META Data
__copyright__  = 'Copyright 2022, CFDeadlines'
__credits__    = ['CFDeadlines (Lead Programmer, Creator)']
__license__    = 'EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)'
__version__    = '1.3.0'
__maintainer__ = 'CFDeadlines'
__email__      = 'cookm0803@gmail.com'
__status__     = 'Open'

################
#  Exceptions  #
################
class DoNotRunDirectly(Exception):
	pass

class SkillError(Exception):
	pass

class ClueError(Exception):
	pass

class HiscoresError(Exception):
	pass

class LMSArenaError(Exception):
	pass	

class BossError(Exception):
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
		self.username = username.lower()
		self.accountType = actype.upper()
		self.__getHTTPResponse()

	def __getHTTPResponse(self):
		"""getHTTPResponse() method

		The getHTTPResponse() method communicates with the OSRS Hiscores API
		and supplies the required information from self.username and
		self.actype to pull the given users stats and hiscore information.

		Args:
			self

		Returns:
			None

		Triggers:
			self.__processResponse(): This method is always triggered, regardless
			                        of whether or not the query to the API returned
						successfully or not.
		"""
		conn = http.client.HTTPSConnection('secure.runescape.com')
		if self.accountType == 'N':
			conn.request("GET", "/m=hiscore_oldschool/index_lite.ws?player={}".format(self.username.replace(' ','%20')))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == 'IM':
			conn.request("GET", "/m=hiscore_oldschool_ironman/index_lite.ws?player={}".format(self.username.replace(' ','%20')))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == "UIM":
			conn.request("GET", "/m=hiscore_oldschool_ultimate/index_lite.ws?player={}".format(self.username.replace(' ','%20')))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == "HIM":
			conn.request("GET", "/m=hiscore_oldschool_hardcore_ironman/index_lite.ws?player={}".format(self.username.replace(' ','%20')))
			self.response = conn.getresponse()
			self.status = self.response.status
		self.__processResponse()

	def __processResponse(self):
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
			self.errorMsg = "Player name given not found in account type provided.  Valid account types are, 'N' (Normal), 'IM' (Iron Man), 'UIM' (Ultimate Iron Man), 'HIM' (Hardcore Iron Man)"
			self.error()
		else:
			self.data = self.response.read().decode('ascii')
			self.__parseData()

	def __parseSkills(self):
		subset = {}
		# Totals
		info = {}
		info['rank'] = self.data[0]
		info['level'] = self.data[1]
		info['experience'] = self.data[2]
		subset['total'] = info

		self.__skills = [
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

		for skill in self.__skills:
			for item in self.__parsed_data:
				info_list = item.split(",")
				info = {}
				info['rank'] = int(info_list[0])
				info['level'] = int(info_list[1])
				info['experience'] = int(info_list[2])

				# calculate xp to next level
				level = info['level'] + 1
				info['next_level_exp'] = math.floor(sum((math.floor(level + 300 * (2 ** (level / 7.0))) for level in range(1, level)))/4)
				info['exp_to_next_level'] = int(info['next_level_exp'] - info['experience'])
				subset[skill] = info
				self.__parsed_data.remove(item)
				break

		self.stats[self.username] = subset

	def __parseBountyHunter(self):
		subset = {}
		self.__bounty_ranks = [
			"hunter",
			"rogue"
		]

		for bounty in self.__bounty_ranks:
			for item in self.__parsed_data:
				info_list = item.split(",")
				info = {}
				info["rank"] = int(info_list[0])
				info["score"] = int(info_list[1])
				subset[bounty] = info
				self.__parsed_data.remove(item)
				break

		self.bounties[self.username] = subset


	def __parseClues(self):
		subset = {}
		self.__clue_tiers = [
			"all",
			"beginner",
			"easy",
			"medium",
			"hard",
			"elite",
			"master"
		]
		for clue in self.__clue_tiers:
			for item in self.__parsed_data:
				info_list = item.split(",")
				info = {}
				info["rank"] = int(info_list[0])
				info["score"] = int(info_list[1])
				subset[clue] = info
				self.__parsed_data.remove(item)
				break

		self.clues[self.username] = subset

	def __parseLMS(self):
		subset = {}

		# I partake in none of this so if someone wants to clear this up
		# please feel free to
		self.__lms_arena_stuff = [
			"lms_rank",
			"pvp_arena_rank",
			"soul_wars_zeal"
		]

		for activity in self.__lms_arena_stuff:
			for item in self.__parsed_data:
				info_list = item.split(",")
				info = {}
				info["rank"] = int(info_list[0])
				info["score"] = int(info_list[1])
				subset[activity] = info
				self.__parsed_data.remove(item)
				break

		self.lms_arenas_sw[self.username] = subset

	def __parseBosses(self):
		subset = {}

		self.__bosses = [
			"rifts_closed",
			"abyssal_sire",
			"alchemical_hydra",
			"barrows_chests",
			"bryophyta",
			"callisto",
			"cerberus",
			"chambers_of_xeric",
			"chambers_of_xeric_challenge",
			"chaos_elemental",
			"chaos_fanatic",
			"commander_zilyana",
			"corporeal_beast",
			"crazy_archaeologist",
			"dagannoth_prime",
			"dagannoth_rex",
			"dagannoth_supreme",
			"deranged_archaeologist",
			"general_graardor",
			"giant_mole",
			"grotesque_guardians",
			"hesporti",
			"kalphite_queen",
			"king_black_dragon",
			"kraken",
			"kreearra",
			"kril_tsutsaroth",
			"mimic",
			"nex",
			"nightmare",
			"phosanis_nightmare",
			"obor",
			"sarachnis",
			"scorpia",
			"skotizo",
			"tempoross",
			"gauntlet",
			"corrupted_gauntlet",
			"theatre_of_blood",
			"theatre_of_blood_hard",
			"thermonuclear_smoke_devil",
			"tombs_of_amascut",
			"tombs_of_amascut_expert",
			"zuk",
			"jad",
			"venenatis",
			"vetion",
			"vorkath",
			"wintertodt",
			"zalcano",
			"zulrah"
		]

		for boss in self.__bosses:
			for item in self.__parsed_data:
				info_list = item.split(",")
				info = {}
				info["rank"] = int(info_list[0])
				info["score"] = int(info_list[1])
				subset[boss] = info
				self.__parsed_data.remove(item)
				break

		self.bosses[self.username] = subset


	def __parseData(self):
		self.stats = {}
		self.bounties = {}
		self.clues = {}
		self.lms_arenas_sw = {}
		self.raids = {}
		self.bosses = {}

		# Prep data for parsing
		self.__parsed_data = self.data.split("\n")
		self.__parsed_data.pop(0) # remove totals section

		self.__parseSkills()

		# Skip over unused values for most people
		self.__parsed_data.pop(0) # Skip over "unknown" (open issue if you know it)

		self.__parseBountyHunter()
		self.__parseClues()
		self.__parseLMS()
		self.__parseBosses()


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
				raise SkillError("stype must be 'rank','level', or experience'")
			else:
				return self.stats[self.username][skill.lower()][stype.lower()]
		except KeyError as KE:
			raise SkillError("ERROR: skill {} does not exist".format(KE))

	def clue(self, clue, clue_type: str = 'score'):
		"""clue() method

		The clue() method allows for users to access their clue scores
		and ranks by providing the tier of clue they want to get info about

		Args:
			clue (str): The OSRS Clue type to get information on

			clue_type (str): either "rank" or "score"  If not supplied
							 it assumes "score"

		Returns:
			self.clues[username][clue_tier][clue_type] (int)
		"""
		try:
			if clue_type.lower() not in ["rank","score"]:
				raise ClueError("clue_type must be 'rank' or 'score'")
			else:
				return self.clues[self.username][clue.lower()][clue_type.lower()]
		except KeyError as KE:
			raise ClueError("ERROR: clue {} does not exist".format(KE))

	def bounty(self, bounty, bounty_type: str = 'score'):
		"""bounty() method

		The bounty() method allows for users to access their bounty scores
		and ranks by providing the bounty they want to get info about

		Args:
			bounty (str): The OSRS bounty type to get information on
						  either "hunter", or "rogue"

			bounty_type (str): either "rank" or "score"  If not supplied
							 it assumes "score"

		Returns:
			self.bounties[username][bounty_tier][bounty_type] (int)
		"""
		try:
			if bounty_type.lower() not in ["rank","score"]:
				raise BountyError("bounty_type must be 'rank' or 'score'")
			else:
				return self.bounties[self.username][bounty.lower()][bounty_type.lower()]
		except KeyError as KE:
			raise BountyError("ERROR: bounty {} does not exist".format(KE))

	def lms_arena_sw(self, activity_type, info_type: str = 'score'):
		try:
			if info_type.lower() not in ["rank","score"]:
				raise LMSArenaError("info_type must be 'rank' or 'score'")
			else:
				return self.lms_arenas_sw[self.username][activity_type.lower()][info_type.lower()]
		except KeyError as KE:
			raise LMSArenaError("ERROR: activity_type does not exist".format(KE))

	def boss(self, boss_name, info_type: str = 'score'):
		try:
			if info_type.lower() not in ["rank","score"]:
				raise BossError("info_type must be 'rank' or 'score'")
			else:
				return self.bosses[self.username][boss_name.lower()][info_type.lower()]
		except KeyError as KE:
			raise BossError("ERROR: boss_name does not exist")

	def error(self):
		HiscoresError("Error occurred: {}".format(self.errorMsg))
	##########################
	#  END: Hiscores Object  #
	##########################

	##########################
	#  TESTING METHODS       #
	##########################
	def getSkillsGenerator(self):
		for skill in self.__skills:
			yield skill

	def getPVPGenerator(self):
		for activity in self.__lms_arena_stuff:
			yield activity

	def getClueGenerator(self):
		for clue in self.__clue_tiers:
			yield clue

	def getBountyGenerator(self):
		for bounty in self.__bounty_ranks:
			yield bounty

	def getBossGenerator(self):
		for boss in self.__bosses:
			yield boss
