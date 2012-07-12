BigBrotherBot Weapon Restriction Plugin for Battlefield 3
=========================================================

http://www.bigbrotherbot.net

Description
-----------

By using this plugin you can restrict the use of weapons of your choice on a BF3 server.

Warning!
--------
The use of this plugin may violate EA's Rules of Conduct for server administrators, for more info see http://bit.ly/bfroc
This plugin works only for Battlefield 3

Changelog
---------

v1.0
  Initial release

Installation
------------

- copy weaponrestrictbf3.py into b3/extplugins
- copy weaponrestrictbf3.ini into your b3/extplugins/conf folder
- edit weaponrestrictbf3.ini with your preferred settings (explanations included in config file)
- add the following line to plugins section of your b3 config file::

   <plugin name="weaponrestrictbf3" config="@b3/extplugins/conf/weaponrestrictbf3.ini"/>

Commands
--------

!weaponrestrict <on | off>
  Enable/disable weapon restriction

!restricted or !rw
  List restricted weapons
 
Support
-------

see the B3 forums http://forum.bigbrotherbot.net/

**Author:** Freelander - freelander@bigbrotherbot.net - http://www.bigbrotherbot.net