#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  secret.py
#  
#  Copyright 2017 Keaton Brown <linux.keaton@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
########################################################################
#
# THIS FILE CONTAINS SENSITIVE INFORMATION. Do not make it public.
#                       You have been warned...
#
########################################################################
#
# Fill in the variables as instructed. Put information inside the 
# apostrophes where applicable. If you must use an apostrophe
# for any reason (i.e. in your password), you must escape
# the character using a '\'. For example, if your password is
# Stacy'sMom, you should enter it below as 'Stacy\'sMom'.
#
########################################################################

# This is your personal reddit username. Do not include '/u/'.
# This is used for the user agent for the Reddit API.
# ( 'spez' not '/u/spez' or 'u/spez' )
me = ''

# This is the subreddit for the exchange. Do not include '/r/'.
# ( 'ClosetSanta' not '/r/ClosetSanta' or 'r/ClosetSanta' )
mySubreddit = ''

# These are for the bot's account. Do not include '/u/', as above.
# See the 'Getting Started' section if you don't know how to get these:
# https://github.com/reddit/reddit/wiki/OAuth2
username = ''
password = ''
client_id = ''
client_secret = ''

# Time *in seconds* to wait between refreshing the bot.
# You may use mathematical operators like +-*/ and parenthesis.
# (as an example, 5*60 and 300 are both 5 minutes)
# Alternatively, if you prefer using cron, set this to 0.
# This should not be in apostrophes.
sleepTime = 5*60
