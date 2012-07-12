# -*- encoding: utf-8 -*-
from tests import prepare_fakeparser_for_tests
prepare_fakeparser_for_tests()

import os
import time
import b3
from b3.fake import fakeConsole, joe, simon, superadmin, FakeClient
from weaponrestrictbf3 import Weaponrestrictbf3Plugin
from b3.config import CfgConfigParser

conf = CfgConfigParser()
conf.loadFromString("""
[commands]
weaponrestrict: 80
restricted-rw: 0
[messages]
warn_kick_message: 'Using %s is not allowed on this server. Please type !rw to see a list of restricted weapons'
[punish_method]
punish_method: 2
warn_duration: 1h
[restricted_weapons]
restricted_weapons: RPG-7, SMAW, M320, M26Mass
[whitelist_gametypes]
whitelist_gametypes: GunMaster0, ConquestLarge0, ConquestSmall0
""")
# make B3 think it has a config file on the filesystem
conf.fileName = os.path.join(os.path.dirname(__file__), '../extplugins/conf/weaponrestrict.ini')

p = Weaponrestrictbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
print p.warn_duration
