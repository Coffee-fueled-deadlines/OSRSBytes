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
__version__    = '1.2.3'
__maintainer__ = 'Markis Cook'
__email__      = 'cookm0803@gmail.com'
__status__     = 'Open'

################
#  Exceptions  #
################
class DoNotRunDirectly(Exception):
	"""DoNotRunDirectly Exception

	This exception is called when the Items.py application is run directly
	as main instead of being imported.
	"""
	pass

class ItemNotValid(Exception):
	"""ItemNotValid Exception

	This exception is called when the itemname or id that is passed to getitem
	is not valid or doesn't exist.
	"""
	pass

class APIDown(Exception):
	"""APIDown Exception

	The APIDown Exception is called whenever the ItemDict fails to fetch from
	the specified URL.
	"""
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

	The Items Object accepts no arguments.  The Items object is  a dictionary of all OSRS Items.
	Dictionary is ordered by ['itemname'] as key.  Items can be entered as name or itemid and are
	converted.  While both are accepted, itemname is 'faster' since the dictionary is keyed by it
	and entering an itemid requires a bit of searching.

	Args:
		None

	Returns:
		None
	"""

	def __init__(self):
		# Grand Exchange item lookup Initialization will go here
		req, buylims = self.__getHTTPRequest()
		self.itemname = self.__parseResponseByItemName(req, buylims)
		if not (self.itemname):
			raise APIDown('The rsbuddy market API appears to be down')

	def __getHTTPRequest(self):
		"""getHTTPRequest method

		The getHTTPRequest method is responsible for establishing a request
		with the rsbuddy API.

		Args:
			None

		Returns:
			string: API JSON Response in String format
		"""
		rsBuddyAPI = 'https://rsbuddy.com/exchange/summary.json'
		osrs_wiki_buylims = 'https://oldschool.runescape.wiki/api.php?action=query&prop=revisions&rvprop=content&titles=Grand_Exchange/Buying_limits&format=json'

		return urllib.request.Request(rsBuddyAPI, headers={'User-Agent': 'Mozilla/5.0'}), urllib.request.Request(osrs_wiki_buylims, headers={'User-Agent': 'Mozilla/5.0'})

	def __parseBuyLimits(self, unparsedJSON):
		"""parseBuyLimits method

		The parseBuyLimits method is responsible for parsing the json data retreived from
		the OSRS wiki page associated with buy orders.

		Args:
			unparsedJSON : dict : The unparsed json dictionary received from the osrs wiki

		Returns:
			buyLimitDict : dict : A properly parsed dictionary needed by the rest of the 
			                      __parseResponseByItemName method.

		"""
		for i,x in unparsedJSON['query']['pages'].items():
			buyLimitString = x['revisions'][0]
		buyLimitString = buyLimitString['*'].replace("\n","").replace("]]","").replace("[[","")
		buyLimitString = buyLimitString.split("|}==Changes")[0].split("|Buy limit|-|")[1]
		buyLimitList = buyLimitString.split("|-|")
		buyLimitDict = {}
		for item in buyLimitList:
			try:
				itemsplit = item.split("|")
				buyLimitDict[itemsplit[0].lower()] = {'buy_limit':int(itemsplit[1])}
			except:
				pass # Skip anything that is wonky.
		return buyLimitDict

	def __parseResponseByItemName(self, req, buylims):
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
			unparsedBuyLims = json.loads(r.decode('utf-8'))
			parsedBuyLims   = self.__parseBuyLimits(unparsedBuyLims)
		except:
			pass # Passing this on fail prevents library from crashing

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

	def __normalize_input(self, itemNameOrID: str):
		"""normalize_input method

		The normalize_input method replaces the old system that required OSRSBytes to create two separate dictionaries,
		one keyed with itemid and the other keyed with itemname.  Instead, we have one dictionary keyed by Itemname and
		normalize_input(itemNameOrID) converts it to the appropriate format.

		Args:
			itemNameOrID: str|int : The item's name or its ID

		Returns:
			String : The name of the item in string format
		"""
		if type(itemNameOrID) == int or itemNameOrID.isnumeric():
			return self.getName(str(itemNameOrID))
		return itemNameOrID

	def getItem(self, itemNameOrID: str):
		"""getItem Method

		The getItem method, when supplied an Item Name or Item ID, returns a dictionary containing
		all item information.
		"""
		try:
			return self.itemname[self.__normalize_input(str(itemNameOrID).lower())]
		except KeyError:
			raise ItemNotValid("{} is not a valid item and was not found.".format(itemNameOrID))

		
	def getName(self, itemNameOrID: str):
		"""getName Method

		The getName method, when supplied an Item Name or Item ID, returns a string value containing
		the in-game name of the Item.
		"""
		for itemid, x in self.itemname.items():
			if str(x['id']) == itemNameOrID or str(x['name']).lower() == itemNameOrID:
				return x['name'].lower()

	def getItemID(self, itemNameOrID: str):
		"""getItemID method

		The getItemID method, when supplied an Item Name or Item ID, returns a string value containing
		the Item ID of the Item.
		"""
		return self.itemname[itemNameOrID.lower()]['id']		

	def getBuyAverage(self, itemNameOrID: str):
		"""getBuyAverage Method

		The getBuyAverage method, when supplied an Item Name or Item ID, returns an integer value containing
		the Item's current in-game buy value.
		"""
		return self.itemname[self.__normalize_input(str(itemNameOrID).lower())]['buy_average']

	def getSellAverage(self, itemNameOrID: str):
		"""getSellAverage Method

		The getSellAverage method, when supplied an Item Name or Item ID, returns an integer value containing
		the Item's current in-game sell value.		
		"""
		return self.itemname[self.__normalize_input(str(itemNameOrID).lower())]['sell_average']

	def getBuyQuantity(self, itemNameOrID: str):
		"""getBuyQuantity Method

		The getBuyQuantity method, when supplied an Item Name or Item ID, returns an integer value containing
		the Item's current number of in-game buy orders.
		"""
		return self.itemname[self.__normalize_input(str(itemNameOrID).lower())]['buy_quantity']

	def getSellQuantity(self, itemNameOrID: str):
		"""getSellQuantity Method

		The getSellQuantity method, when supplied an Item Name or Item ID, returns an integer value containing
		the Item's current number of in-game sell orders.
		"""		
		return self.itemname[self.__normalize_input(str(itemNameOrID).lower())]['sell_quantity']
		
	def getBuyLimit(self, itemNameOrID: str):
		"""getBuyLimit Method

		The getBuyLimit method, when supplied an Item Name or Item ID, returns an integer value containing
		the Grand Exchange Buy Limit for that item.  If a buy limit is not found, this method returns None
		"""
		try:
			return self.itemname[self.__normalize_input(str(itemNameOrID).lower())]['buy_limit']
		except:
			return False

	def getShopPrice(self, itemNameOrID: str):
		"""getShipPrice Method

		The getShopPrice method, when supplied an Item Name or Item ID, returns an integer value containing
		the in-game item's shop price
		"""
		return self.itemname[self.__normalize_input(str(itemNameOrID).lower())]['sp']

	def getLowAlchValue(self, itemNameOrID: str):
		"""getLowAlchValue Method

		The getLowAlchValue method, when supplied an Item Name or Item ID, returns an integer value containing
		the coin return value of casting Low Alchemy on the in-game item.
		"""
		return math.ceil(self.itemname[self.__normalize_input(str(itemNameOrID).lower())]['sp']*.40)

	def getHighAlchValue(self, itemNameOrID: str):
		"""getHighAlchValue Method

		The getHighAlchValue method, when supplied an Item Name or Item ID, returns an integer value containing
		the coin return value of casting High Alchemy on the in-game item.		
		"""
		return math.ceil(self.itemname[self.__normalize_input(str(itemNameOrID).lower())]['sp']*.60)

	def isMembers(self, itemNameOrID: str):
		"""isMembers Method

		The isMembers method, when supplied with an Item Name or Item ID, returns a boolean value dependant
		on whether the supplied item is Members Only or not.
		"""
		return bool(self.itemname[self.__normalize_input(str(itemNameOrID).lower())]['members'])
	##########################
	#  END: Items Object     #
	##########################