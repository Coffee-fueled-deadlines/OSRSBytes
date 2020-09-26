# OSRSBytes
![version](https://img.shields.io/pypi/v/OSRSBytes?style=for-the-badge)
![downloads](https://img.shields.io/pypi/dm/OSRSBytes?style=for-the-badge)<br>
![size](https://img.shields.io/github/languages/code-size/coffee-fueled-deadlines/osrsbytes?style=for-the-badge)
![platform & version support](https://img.shields.io/pypi/pyversions/OSRSBytes?style=for-the-badge)


## Updates

[update 20200925]

__Currently implemented in v1.2.0__:
* Hiscores Shelve-caching (reduces the number of calls to the api).

__Fixes currently implemented in v1.2.0__:
* Previously, ItemID and ItemName each had their own dictionary to allow users to search by either ItemID or ItemName.  This was dumb of me, so I instead implemented one dictionary that was keyed by ItemName.  You can still search by ItemID thanks to the `self.__normalize_input()` method which will ensure that anything you input is converted to item name.  If you put in `int(1213)` or `str(1213)` the method will, ultimately, return `"rune dagger"`

## Introduction

OSRSBytes is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information from RSBuddy.

### Installation:
```
pip install OSRSBytes
```

### Upgrade
```
pip install OSRSBytes --upgrade
```

### Example Invocation (Hiscores)
```python
from OSRSBytes import Hiscores

user = Hiscores('Zezima', 'N')

# Lets display some information
print("Current level:", user.skill('attack', 'level'))
print("Current rank:", user.skill('attack', 'rank'))
print("Current exp:", user.skill('attack', 'experience'))
print("Exp remaining:", user.skill('attack','exp_to_next_level'))
```

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
