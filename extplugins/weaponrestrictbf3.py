# -*- coding: utf-8 -*-
#
# BF3 Weapon Restrcition Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Based on antinoob.py by
# Gamers 4 Gamers (http://g4g.pl)
# Copyright (C) 2009 Anubis
# 
# Modified for BFBC2 by
# Durzo <durzo@badcompany2.com.au>
#
# Modified for BF3 by
# Freelander <freelander@bigbrotherbot.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# CHANGELOG
#    12/07/2012 - 1.0 - Freelander
#    -- Initial release


__version__ = '1.0'
__author__  = 'Freelander'

import b3
import ConfigParser
import re
import string
import b3.events
from b3.plugin import Plugin

#--------------------------------------------------------------------------------------------------

class Weaponrestrictbf3Plugin(b3.plugin.Plugin):

    def __init__(self, console, config=None):
        self.restriction_status = True
        self.punish_method = 1
        self.warn_duration = '1h'
        self._adminPlugin = None
        self._current_gametype = None
        self._restrictedweapons = []
        self._whitelistgametypes = []
        Plugin.__init__(self, console, config)

################################################################################################################
#
#    Plugin interface implementation
#
################################################################################################################

    def startup(self):
        self._adminPlugin = self.console.getPlugin('admin')
        self._registerCommands()
        self.registerEvent(b3.events.EVT_CLIENT_KILL)
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)
        self.registerEvent(b3.events.EVT_GAME_MAP_CHANGE)
        self.info('WARNING: The use of this plugin may violate EA\'s Rules of Conduct for server administrators, for more info see http://bit.ly/bfroc')

    #---------------------------------------------------------------------------#

    def onLoadConfig(self):
        self.debug('Loading Configuration Started')
        self.load_messages()
        self.load_punish_method()
        self.load_warn_durarion()
        self.load_restricted_weapons()
        self.load_whitelist_gametypes()
        self.debug('Loading Configuration Finished')

    #---------------------------------------------------------------------------#

    def onEvent(self, event):
        if event.type == b3.events.EVT_GAME_ROUND_START or event.type == b3.events.EVT_GAME_MAP_CHANGE:
            self.get_current_gametype()
        elif event.type == b3.events.EVT_CLIENT_KILL or event.type == b3.events.EVT_CLIENT_KILL_TEAM:
            weaponname = event.data[1]
            self.debug('Weapon: %s' % weaponname)
            self.check_weapon(weaponname, event.client)

    #---------------------------------------------------------------------------#

    def _getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func
        return None

    #---------------------------------------------------------------------------#

    def _registerCommands(self):
        # register our commands
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp
                func = self._getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

################################################################################################################
#
#    Config Options Methods
#
################################################################################################################

    def load_messages(self):
        try:
            self._warnkickmsg = self.config.get('messages', 'warn_kick_message')
        except ConfigParser.NoOptionError:
            self.debug('Cannot load messages from config file! Using default message')
            self._warnkickmsg = 'Using %s is not allowed on this server. Please type !rw to see a list of restricted weapons'

    #---------------------------------------------------------------------------#

    def load_punish_method(self):
        try:
            self.punish_method = self.config.getint('punish_method', 'punish_method')
            if self.punish_method == 1:
                self.debug('Punish Method Loaded: >> Kick <<')
            if self.punish_method == 2:
                self.debug('Punish Method Loaded: >> Warn <<')
        except ConfigParser.NoOptionError:
            self.debug('Cannot load punish method. Using default: Kick')
        except ValueError:
            self.debug('Cannot load punish method. Empty or non-numeric value detected. Using default: Kick')

    #---------------------------------------------------------------------------#

    def load_warn_durarion(self):
        if self.punish_method == 1:
            return False

        try:
            self.warn_duration = self.config.get('punish_method', 'warn_duration')
            self.debug('Warn Duration Loaded: >> %s <<' % self.warn_duration)
        except ConfigParser.NoOptionError:
            self.debug('Cannot load warn duration. Using default value "1h"')

    #---------------------------------------------------------------------------#

    def load_restricted_weapons(self):
        try:
            i = self.config.get('restricted_weapons', 'restricted_weapons')
            weapons = re.split(',', i)
            for weapon in weapons:
                weapon = weapon.strip()
                self._restrictedweapons.append(weapon)
                self.info('Restricted Weapon Loaded: >> %s <<' % weapon)
        except ConfigParser.NoOptionError:
            self.debug('Cannot load restricted weapons!')

    #---------------------------------------------------------------------------#

    def load_whitelist_gametypes(self):
        try:
            i = self.config.get('whitelist_gametypes', 'whitelist_gametypes')
            gametypes = re.split(',', i)
            for gametype in gametypes:
                gametype = gametype.strip()
                self._whitelistgametypes.append(gametype)
                self.info('Whitelist Gametype Loaded: >> %s <<' % gametype)
        except ConfigParser.NoOptionError:
            self.debug('Cannot load white listed gametypes')

################################################################################################################
#
#   Commands implementations
#
################################################################################################################

    def cmd_weaponrestrict(self, data, client, cmd=None):
        '''
        <on | off> Enables/disables weapon restriction
        '''
        data = data.lower()

        if data not in ('on', 'off'):
            client.message("Invalid data, expecting 'on' or 'off'")
        elif data == 'on':
            self.restriction_status = True
            client.message('Weapon Restriction is turned on')
        elif data == 'off':
            self.restriction_status = False
            client.message('Weapon Restriction is turned off')

    #---------------------------------------------------------------------------#

    def cmd_restricted(self, data, client, cmd=None):
        '''
        List restricted weapons
        '''
        if self.restriction_status is False:
            client.message("Weapon restriction is currently disabled, all weapons are allowed")
        elif len(self._restrictedweapons) == 0 or self._restrictedweapons == ['']:
            client.message("No restricted weapons found! All weapons are allowed!")
        else:
            client.message("Restricted Weapon(s): %s" % string.join(self._restrictedweapons, ', '))

################################################################################################################
#
#    Other Methods
#
################################################################################################################

    def check_weapon(self, weaponname, player):
        if self._current_gametype not in self._whitelistgametypes:
            if self.restriction_status is True:
                if weaponname in self._restrictedweapons:
                    self.info('Restricted Weapon: %s used by %s' % (str(weaponname), str(player.name)))
                    if self.punish_method == 1:
                        self.kick_player_for_restricted_weapon(player, weaponname)
                    elif self.punish_method == 2:
                        self.warn_player_for_restricted_weapon(player, weaponname)
            else:
                self.debug('Weapon Restriction is currently disabled. Ignoring kick')
        else:
            self.debug('Current Gametype (%s) is in Whitelist. Ignoring weapon restriction' % self._current_gametype)

    #---------------------------------------------------------------------------#

    def kick_player_for_restricted_weapon(self, player, weaponname):
        if player and weaponname:
            msg = self._warnkickmsg % weaponname
            self.debug('%s was kicked for using %s' % (player.name, weaponname))
            player.kick(reason=msg, keyword="weaponrestrict")

    #---------------------------------------------------------------------------#

    def warn_player_for_restricted_weapon(self, player, weaponname):
        if player and weaponname:
            msg = self._warnkickmsg % weaponname
            self.debug('%s was warned for using %s' % (player.name, weaponname))
            player.warn(duration=self.warn_duration, warning=msg, keyword="weaponrestrict")

    #---------------------------------------------------------------------------#
    def get_current_gametype(self):
        self._current_gametype = self.console.game.gameType
        self.debug('Current gametype is %s' % self._current_gametype)
        return self._current_gametype
