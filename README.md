# OSRSBytes (v1.1.0)

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
