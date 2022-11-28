# OSRSBytes (v1.3.0)
![version](https://img.shields.io/pypi/v/OSRSBytes?style=for-the-badge)
![downloads](https://img.shields.io/pypi/dm/OSRSBytes?style=for-the-badge)<br>
![size](https://img.shields.io/github/languages/code-size/coffee-fueled-deadlines/osrsbytes?style=for-the-badge)
![platform & version support](https://img.shields.io/pypi/pyversions/OSRSBytes?style=for-the-badge)
=======
## Production Branch
[update20220125]
__Added OSRS Wiki to Items module in v1.2.5__:
* Added the OSRS Wiki API to the Items Module.

[update 20210710]
__Fixes implemented in v1.2.4__:
* Escape username to avoid getting errors for usernames that contain spaces.
* Fixed bug in setup.py causing a manual install to fail and matched version numbers to 1.2.4.

[update 20201004]
__Bug Fix__:
* Fixed a bug that caused the API to appear to be down due to a messup in parsing.  Update OSRSBytes with `pip install OSRSBytes --upgrade` to fix this bug.

[update 20200925]

__Currently implemented in v1.2.2__:
* Hiscores Shelve-caching (reduces the number of calls to the api).

__Fixes currently implemented in v1.2.2__:
* Previously, ItemID and ItemName each had their own dictionary to allow users to search by either ItemID or ItemName.  This was dumb of me, so I instead implemented one dictionary that was keyed by ItemName.  You can still search by ItemID thanks to the `self.__normalize_input()` method which will ensure that anything you input is converted to item name.  If you put in `int(1213)` or `str(1213)` the method will, ultimately, return `"rune dagger"`

## Introduction
> 
> OSRSBytes is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information from RSBuddy.
 
### Installation:
> ```cmd
> pip install OSRSBytes
> ```

### Upgrade
> ```cmd
> pip install OSRSBytes --upgrade
> ```

### Example Invocation (Hiscores)
> The OSRSBytes library contains caching on Hiscores to improve performance.  Caching is disabled by default and must be enabled when initializing the hiscores object.  Note that default TTL of cache is `3600` seconds or `1` hour.
> Example without Caching
> ```python
> ######################
> # No Caching Example #
> ######################
> from OSRSBytes import Hiscores
> 
> user = Hiscores('Zezima')
> 
> # Lets display some information
> print("Current level:", user.skill('attack', 'level'))
> print("Current rank:", user.skill('attack', 'rank'))
> print("Current exp:", user.skill('attack', 'experience'))
> print("Exp remaining:", user.skill('attack','exp_to_next_level'))
> ```
> 
> Example utilizing Caching
> ```python
> ###################
> # Caching Example #
> ###################
> from OSRSBytes import Hiscores
> 
> user = Hiscores('zezima', caching=True)
>  
> # Lets display some information
> print("Current level:", user.skill('attack', 'level'))
> print("Current rank:", user.skill('attack', 'rank'))
> print("Current exp:", user.skill('attack', 'experience'))
> print("Exp remaining:", user.skill('attack','exp_to_next_level'))
> 
> # Reinitializing the Hiscores class is quick now, as we already have the information cached
> user = Hiscores('zezima', caching=True)
> # user = Hiscores('zezima', caching=True, cacheTTL=7200) # Optional custom cacheTTL
> 
> print("Current level:", user.skill('attack', 'level'))
> print("Current rank:", user.skill('attack', 'rank'))
> print("Current exp:", user.skill('attack', 'experience'))
> print("Exp remaining:", user.skill('attack','exp_to_next_level'))
> 
> # Lets get the current time left in the cache (in seconds) for Zezima
> print("TTL for Cache: ", user.getCacheTTLRemaining()) # rounded up to nearest second
> ```

### Example Invocation (HiscoresCache)
> The OSRSBytes library allows for you to directly manage the HiscoresCache independant of the Hiscores module.
> ```python
> ##############################
> # Working with HiscoresCache #
> ##############################
> from OSRSBytes import HiscoresCache
> 
> # Initialize the cache object
> cache = HiscoresCache()
> 
> # Lets clear a large number of expired users from the cache
> cache.clearExpiredCacheEntries()
> print(cache.purgeCounter) # Int
> print(cache.usersDeleted) # List
> 
> # Lets remove a specific user from the HiscoresCache
> if cache.removeFromCache("Zezima"):
>     print("User Removed")
> else:
>     print("User not in cache")
> 
> # Lets completely destroy the cache.  Note that this method completed removes the cache files as well as the
> # cache folder itself.
> cache.destroyCache()
> ```

### Example Invocation (Items)
```python

from OSRSBytes import Items

items = Items()

# Lets get information on this item
print('Is Members:',    items.isMembers('rune dagger'))
print("Item ID:",         items.getItemID('rune dagger'))
    
print('Sell Average:',  items.getSellAverage('rune dagger'))
print('Sell Quantity:', items.getSellQuantity('rune dagger'))

print('Buy Average:',  items.getBuyAverage('rune dagger'))
print('Buy Quantity:', items.getBuyQuantity('rune dagger'))
print('Buy Limit:',    items.getBuyLimit('fire rune'))

print('Shop Price:',      items.getShopPrice('rune dagger'))
print('High Alch Value:', items.getHighAlchValue('rune dagger'))
print('Low Alch Value:',  items.getLowAlchValue('rune dagger'))

# In addition, all items can be called by Item ID as well
print('Item Name:',       items.getName('1213'))
print('Sell Average:',    items.getSellAverage('1213'))
```

### Contributing

Prior to contributing, please consider the following before committing code:

1. Do not leave commented lines in code (i.e. `#print('test')`
1. Try to write your code as cleanly and readable as possible
1. Whenever possible, do not use third party packages, try your hardest to utilize built-in python packages
1. No commits should break previous code functionality.  This means that method names should remain the same and return the same, expected values in the same format.

Thank you for your considerations
