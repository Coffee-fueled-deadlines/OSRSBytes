# OSRSBytes ChangeLog
## Begin-date: 20191230
## Last-Update: 20200201

[update 20221130]
__Updated OSRSBytes to Version 1.3.0__:

[update 20220125]
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

### V. 1.2.0
> 
> Began implementation of OSRSBytes built-in shelve caching.  Caching is currently implemented for `Hiscores` and a new module has been added called, `HiscoresCaching` that allows for direct manipulation of the Cache within reason by users.
> 

### V. 1.1.0 (20191230)
> 
> Reworked the way OSRSBytes is constructed.  Previously it all initialized through `OSRSBytes/__init__.py` but that was confusing and not easily scalable (in my opinion).  I've instead reworked the `__init__.py` to instead call sub-modules (namely `Hiscores.py`, `Items.py`,  and `Utilities.py`).  
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
