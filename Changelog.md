# OSRSBytes ChangeLog
## Begin-date: 20191230

### V. 1.1.0
> 
> Reworked the way OSRSBytes is constructed.  Previously it all initialized through `OSRSBytes/__init__.py` but that was confusing and not > easily scalable (in my opinion).  I've instead reworked the `__init__.py` to instead call sub-modules (namely `Hiscores.py`, `Items.py`,  and `Utilities.py`).  
> 
> The goal of this rework was to make it easier to edit modules without breaking other modules in the process during development and to ensure that functionality (specifically calling of the package) was identical.  Both of these goals where achieved.  Upon upgrading your repo to the newest version, you should find that calling OSRSBytes is the same as it was previously.
> 
> In addition, a small bit of functionality was added to the `Items` class of OSRSBytes.
> 
> ```python
> from OSRSBytes import Items
> 
> items = Items()
> print("Rune Scimitar Item ID: ", items.getItemID("rune scimitar"))
> ```
>
> While note a major addition, it does allow developers that wish to look up Item IDs the ability to do so via the OSRSBytes Library.
>

### END
