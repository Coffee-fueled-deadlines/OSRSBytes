#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
OSRSBytes() is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information.

EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)

Items Module is Responsible for fetching all known OSRS Items.  Any modifications involving Items should
be adjusted and added in the Items Module.
"""

# Generic/Built-in Imports
import json
import math
import urllib.request

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
#  START: Items Object     #
############################
class Items(object):
	"""Items Object

	The Items Object accepts no arguments.  The Items object is, essentially, a collection
	of two dictionaries on all OSRS Items.  The self.itemname dictionary is, as the name
	implies, a dictionary of items with the item's name as it's key.  the self.itemid
	dictionary, likewise, is a dictionary of items sorted by the item's id value.

	While creating two separate dictionaries can take slightly longer, it allows for more
	flexibility in development by giving developer's access to either method that they
	prefer

	Note that Methods prefixed by an underscore (_) would prefer that you stay out of their
	living room.  This means that we'd prefer you don't call them directly and instead let the
	class do it's job with them.  However, we're all consenting adults here, so if you need to
	call them, go ahead I guess.

	Args:
		None

	Returns:
		None
	"""

	def __init__(self):
		# Grand Exchange item lookup Initialization will go here
		req, buylims = self._getHTTPRequest()
		self.itemname = self._parseResponseByItemName(req, buylims)
		self.itemid   = self._parseResponseByItemID(req, buylims)
		if not (self.itemname or self.itemid):
			raise APIDown('The rsbuddy market API appears to be down')

	def _getHTTPRequest(self):
		"""getHTTPRequest method

		The getHTTPRequest method is responsible for establishing a request
		with the rsbuddy API.

		Args:
			None

		Returns:
			string: API JSON Response in String format
		"""
		rsBuddyAPI = 'https://rsbuddy.com/exchange/summary.json'
		githubItemInfo = 'https://raw.githubusercontent.com/Coffee-fueled-deadlines/OSRS-JSON-Item-Information/master/item_information.json'
		return urllib.request.Request(rsBuddyAPI), urllib.request.Request(githubItemInfo)


	def _parseResponseByItemName(self, req, buylims):
		"""parseResponseByItemName method

		The parseResponseByItemName() method is responsible for accepting the
		request esablished by the getHTTPRequest() method and loading it into
		the JSON string parser to convert it to a usable python dictionary.

		Once parsed, the dictionary is iterated through and a new dictionary is
		created with identical information except the key value is replaced with
		the item name instead of the item id.

		Args:
			req: The string request received by the getHTTPRequest() method

		Returns:
			itemDict: A dictionary of OSRS Items keyed with item names
			boolval: Returns false on parse error
		"""
		r = urllib.request.urlopen(req).read()
		try:
			parsedJSON =  json.loads(r.decode('utf-8'))
		except:
			return False
		
		r = urllib.request.urlopen(buylims).read()
		try:
			parsedBuyLims = json.loads(r.decode('utf-8'))
		except:
			return False

		# Lets make this item-set not suck
		itemDict = {}
		for idval in parsedJSON:
			itemDict[parsedJSON[idval]['name'].lower()] = parsedJSON[idval]
			try:
				itemDict[parsedJSON[idval]['name'].lower()]['buy_limit'] = parsedBuyLims[parsedJSON[idval]['name'].lower()]['buy_limit']
			except:
				itemDict[parsedJSON[idval]['name'].lower()]['buy_limit'] = None

		# Return the dictionary
		return itemDict

	def _parseResponseByItemID(self, req, buylims):
		"""parseResponseByItemID method

		The parseResponseByItemID() method is responsible for accepting the
		request established by the getHTTPRequest() method and loading it into
		the JSON string parser to convert it to a usable python dictionary keyed
		with the item ID's of the items.

		Args:
			req: The string request received by the getHTTPRequest() method

		Returns:
			itemDict: dictionary of OSRS Items keyed by item ids
			boolval: Returns false on failure to parse
		"""
		r = urllib.request.urlopen(req).read()
		try:
			parsedJSON = json.loads(r.decode('utf-8'))
		except:
			return False
		
		r = urllib.request.urlopen(buylims).read()
		try:
			parsedBuyLims = json.loads(r.decode('utf-8'))
		except:
			return False
		
		for idval in parsedJSON:
			try:
				if parsedJSON[idval]['name'].lower() == parsedBuyLims[parsedJSON[idval]['name'].lower()]['item_name']:
					parsedJSON[idval]['buy_limit'] = parsedBuyLims[parsedJSON[idval]['name'].lower()]['buy_limit']
			except:
				parsedJSON[idval]['buy_limit'] = None
			
		return parsedJSON

	def getItem(self, itemNameOrID: str):
		"""getItem Method

		The getItem method, when supplied an Item Name or Item ID, returns a dictionary containing
		all item information.
		"""
		try:
			return self.itemname[itemNameOrID.lower()]
		except KeyError:
			return self.itemid[itemNameOrID.lower()]
		
	def getName(self, itemNameOrID: str):
		"""getName Method

		The getName method, when supplied an Item Name or Item ID, returns a string value containing
		the in-game name of the Item.
		"""
		try:
			return self.itemname[itemNameOrID.lower()]['name']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['name']

	def getItemID(self, itemNameOrID: str):
		"""getItemID method

		The getItemID method, when supplied an Item Name or Item ID, returns a string value containing
		the Item ID of the Item.
		"""
		try:
			return self.itemname[itemNameOrID.lower()]['id']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['id']			

	def getBuyAverage(self, itemNameOrID: str):
		"""getBuyAverage Method

		The getBuyAverage method, when supplied an Item Name or Item ID, returns an integer value containing
		the Item's current in-game buy value.
		"""
		try:
			return self.itemname[itemNameOrID.lower()]['buy_average']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['buy_average']

	def getSellAverage(self, itemNameOrID: str):
		"""getSellAverage Method

		The getSellAverage method, when supplied an Item Name or Item ID, returns an integer value containing
		the Item's current in-game sell value.		
		"""
		try:
			return self.itemname[itemNameOrID.lower()]['sell_average']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['sell_average']

	def getBuyQuantity(self, itemNameOrID: str):
		"""getBuyQuantity Method

		The getBuyQuantity method, when supplied an Item Name or Item ID, returns an integer value containing
		the Item's current number of in-game buy orders.
		"""
		try:
			return self.itemname[itemNameOrID.lower()]['buy_quantity']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['buy_quantity']

	def getSellQuantity(self, itemNameOrID: str):
		"""getSellQuantity Method

		The getSellQuantity method, when supplied an Item Name or Item ID, returns an integer value containing
		the Item's current number of in-game sell orders.
		"""		
		try:
			return self.itemname[itemNameOrID.lower()]['sell_quantity']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['sell_quantity']
		
	def getBuyLimit(self, itemNameOrID: str):
		"""getBuyLimit Method

		The getBuyLimit method, when supplied an Item Name or Item ID, returns an integer value containing
		the Grand Exchange Buy Limit for that item.  If a buy limit is not found, this method returns None
		"""
		try:
			return self.itemname[itemNameOrID.lower()]['buy_limit']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['buy_limit']
		except:
			return False

	def getShopPrice(self, itemNameOrID: str):
		"""getShipPrice Method

		The getShopPrice method, when supplied an Item Name or Item ID, returns an integer value containing
		the in-game item's shop price
		"""
		try:
			return self.itemname[itemNameOrID.lower()]['sp']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['sp']

	def getLowAlchValue(self, itemNameOrID: str):
		"""getLowAlchValue Method

		The getLowAlchValue method, when supplied an Item Name or Item ID, returns an integer value containing
		the coin return value of casting Low Alchemy on the in-game item.
		"""
		try:
			return math.ceil(self.itemname[itemNameOrID.lower()]['sp']*.40)
		except KeyError:
			return math.ceil(self.itemid[itemNameOrID.lower()]['sp']*.40)

	def getHighAlchValue(self, itemNameOrID: str):
		"""getHighAlchValue Method

		The getHighAlchValue method, when supplied an Item Name or Item ID, returns an integer value containing
		the coin return value of casting High Alchemy on the in-game item.		
		"""
		try:
			return math.ceil(self.itemname[itemNameOrID.lower()]['sp']*.60)
		except KeyError:
			return math.ceil(self.itemid[itemNameOrID.lower()]['sp']*.60)

	def isMembers(self, itemNameOrID: str):
		"""isMembers Method

		The isMembers method, when supplied with an Item Name or Item ID, returns a boolean value dependant
		on whether the supplied item is Members Only or not.
		"""
		try:
			return bool(self.itemname[itemNameOrID.lower()]['members'])
		except KeyError:
			return bool(self.itemid[itemNameOrID.lower()]['members'])
	##########################
	#  END: Items Object     #
	##########################