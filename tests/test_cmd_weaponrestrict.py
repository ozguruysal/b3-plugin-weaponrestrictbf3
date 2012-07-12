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
[restricted_weapons]
restricted_weapons: RPG-7, SMAW, M320, M26Mass
[whitelist_gametypes]
whitelist_gametypes: GunMaster0, ConquestLarge0, ConquestSmall0, RushLarge0, ConquestAssaultLarge0, ConquestAssaultSmall0, ConquestAssaultSmall1
""")
# make B3 think it has a config file on the filesystem
conf.fileName = os.path.join(os.path.dirname(__file__), '../extplugins/conf/weaponrestrict.ini')

p = Weaponrestrictbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()

joe.connects(cid=1)
superadmin.connects(cid=2)

print "----------- Testing Privilege ------------"
joe.says('!weaponrestrict off')
time.sleep(5)

print "----------- Testing No data ------------"
superadmin.says('!weaponrestrict')
time.sleep(5)

print "----------- Testing wrong data ------------"
superadmin.says('!weaponrestrict ofk')
time.sleep(5)

print "----------- Testing Restriction Off ------------"
superadmin.says('!weaponrestrict off')
time.sleep(5)

print "----------- Testing Kill when Restriction Off ------------"
superadmin.kills(joe, 'M320')
time.sleep(5)

print "----------- Testing Restriction On ------------"
superadmin.says('!weaponrestrict On')
time.sleep(5)

print "----------- Testing Kill when Restriction On ------------"
superadmin.kills(joe, 'M320')
time.sleep(5)