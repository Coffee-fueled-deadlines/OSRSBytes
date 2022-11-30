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

	def __init__(self, application_name = None, application_contact = None):
		self.__application_name = application_name if application_name else "OSRSBytes"
		self.__application_contact = application_contact if application_contact else "info@osrsbytes.com"

		prices, volumes, mappings = self.__getHTTPRequest()
		self.itemname = self.__rectifyWikiResponse(prices, volumes, mappings)
		if not (self.itemname):
			raise APIDown(f'The {api} API appears to be down, please try the other')

	def __getHTTPRequest(self):
		"""getHTTPRequest

		This method is responsible for pulling data from runewiki API's. The
		headers are necessary to get sucessful API requests.

		Args:
			None
		Returns:
			dict latest: The latest pricing info in dictionary format
			dict volumes: The latest trading volumes for items.
			list mappings: Mappings of item info.
		"""
		url_mappings = 'https://prices.runescape.wiki/api/v1/osrs/mapping'
		url_prices = 'https://prices.runescape.wiki/api/v1/osrs/latest'
		url_volumes = 'https://prices.runescape.wiki/api/v1/osrs/volumes'
		headers = {
    		"User-Agent" : "{} - {}".format(self.__application_name, self.__application_contact)
		}


		req = urllib.request.Request(url_mappings, headers=headers)
		f = urllib.request.urlopen(req)
		mappings = json.load(f)

		req = urllib.request.Request(url_prices, headers=headers)
		f = urllib.request.urlopen(req)
		prices = json.load(f)['data']

		req = urllib.request.Request(url_volumes, headers=headers)
		f = urllib.request.urlopen(req)
		volumes = json.load(f)['data']

		return prices, volumes, mappings

	def __rectifyWikiResponse(self, prices, volumes, mappings):
		"""rectifyResponseWithMappings

		This method is responsible for accepting the raw dict response from
		RuneWiki's API and combining them into a servicable json/dict structure.
		Args:
			prices dict: a dictionary of the latest item pricing
			volumes dict: A dictionary of the latest trading volumes
			mappings list: A list of relevant item info
		Returns:
			dict: A rectified dictionary of all available item names.

		NOTE: There are more item mappings than pricing or volumes. So not
				all mappings will have pricing/volume info.
		"""
		rect = {}
		try:
			for item in mappings:
			    item['name'] = item['name'].lower() # Normalize itemnames
			    rect[item['name']] = {}
			    rect[item['name']]['name'] = item['name']
			    rect[item['name']]['id'] = item['id']
			    rect[item['name']]['members'] = item['members']
			    rect[item['name']]['examine'] = item['examine']
			    if 'limit' in item:
			        rect[item['name']]['buy_limit'] = item['limit']
			    if 'lowalch' in item:
			        rect[item['name']]['lowalch'] = item['lowalch']
			    if 'highalch' in item:
			        rect[item['name']]['highalch'] = item['highalch']
			    if 'value' in item:
			        rect[item['name']]['sp'] = item['value']

			for item in rect:
			    if str(rect[item]['id']) in volumes:
			        rect[item]['buy_quantity'] = volumes[str(rect[item]['id'])]
			        rect[item]['sell_quantity'] = volumes[str(rect[item]['id'])]
			    if str(rect[item]['id']) in prices:
			        rect[item]['buy_average'] = prices[str(rect[item]['id'])]['high']
			        rect[item]['sell_average'] = prices[str(rect[item]['id'])]['low']
			return rect
		except:
			return False

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
			if str(x['id']) == str(itemNameOrID) or str(x['name']).lower() == str(itemNameOrID):
				return x['name'].lower()

	def getItemID(self, itemNameOrID: str):
		"""getItemID method

		The getItemID method, when supplied an Item Name or Item ID, returns a string value containing
		the Item ID of the Item.
		"""
		return self.itemname[str(itemNameOrID).lower()]['id']

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