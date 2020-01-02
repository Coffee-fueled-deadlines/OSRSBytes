# OSRSBytes (v1.2.0)

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
> The OSRSBytes v1.2.0 library contains caching on Hiscores to improve performance.  Caching is disabled by default and must be enabled when initializing the hiscores object.  Note that default TTL of cache is `3600` seconds or `1` hour.
> 
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
> print("Current level:", user.skill('attack', 'level'))
> print("Current rank:", user.skill('attack', 'rank'))
> print("Current exp:", user.skill('attack', 'experience'))
> print("Exp remaining:", user.skill('attack','exp_to_next_level'))
> 
> # Lets get the current time left in the cache (in seconds) for Zezima
> print("TTL for Cache: ", user.getCacheTTLRemaining()) # rounded up to nearest second
> ```

### Example Invocation (HiscoresCache)
> The OSRSBytes v1.2.0 library allows for you to directly manage the HiscoresCache independant of the Hiscores module.
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

Thank you for your considerations
