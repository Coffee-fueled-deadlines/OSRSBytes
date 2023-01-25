# OSRSBytes (v1.3.0)
![version](https://img.shields.io/pypi/v/OSRSBytes?style=for-the-badge)
![downloads](https://img.shields.io/pypi/dm/OSRSBytes?style=for-the-badge)<br>
![size](https://img.shields.io/github/languages/code-size/coffee-fueled-deadlines/osrsbytes?style=for-the-badge)
![platform & version support](https://img.shields.io/pypi/pyversions/OSRSBytes?style=for-the-badge)
=======
## Introduction
> 
> OSRSBytes is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information from RuneLite/Wiki.
 
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
> from OSRSBytes import Hiscores
> 
> user = Hiscores('Zezima')
> 
> # Lets display some information
> print("Current level:", user.skill('attack', 'level'))
> print("Current rank:", user.skill('attack', 'rank'))
> print("Current exp:", user.skill('attack', 'experience'))
> print("Exp remaining:", user.skill('attack','exp_to_next_level'))
> 
> # Lets display some Boss information
> print("Wintertodt Kills:", user.boss("wintertodt", "score"))
> 
> # Lets display some Clue Hiscores
> print("Medium clues done:", user.clue("medium", "score"))
> ```

### Example Invocation (Items)
> ```python
> 
> from OSRSBytes import Items
> 
> items = Items()
> 
> # Lets get information on this item
> print('Is Members:',    items.isMembers('rune dagger'))
> print("Item ID:",         items.getItemID('rune dagger'))
>     
> print('Sell Average:',  items.getSellAverage('rune dagger'))
> print('Sell Quantity:', items.getSellQuantity('rune dagger'))
> 
> print('Buy Average:',  items.getBuyAverage('rune dagger'))
> print('Buy Quantity:', items.getBuyQuantity('rune dagger'))
> print('Buy Limit:',    items.getBuyLimit('fire rune'))
> 
> print('Shop Price:',      items.getShopPrice('rune dagger'))
> print('High Alch Value:', items.getHighAlchValue('rune dagger'))
> print('Low Alch Value:',  items.getLowAlchValue('rune dagger'))
> 
> # In addition, all items can be called by Item ID as well
> print('Item Name:',       items.getName('1213'))
> print('Sell Average:',    items.getSellAverage('1213'))
> 
> # Lets update all of the item information after some time has passed
> items.update()
> 
> # Lets get some new, up-to-date information
> print('Sell Average:', items.getSellAverage('rune dagger')
> ```

### Contributing
> Prior to contributing, please consider the following before committing code:
> 
> 1. Do not leave commented lines in code (i.e. `#print('test')`
> 1. Try to write your code as cleanly and readable as possible
> 1. Whenever possible, do not use third party packages, try your hardest to utilize built-in python packages
> 1. No commits should break previous code functionality.  This means that method names should remain the same and return the same, expected values in the same format.
> 1. **NEW**: All code should be indented with spaces rather than tabs.
> 1. **NEW**: All code should be pushed to dev branch instead of master branch.  All pull requests sent to master will be rejected.
> 
> Thank you for your considerations
