#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  RSSB.py
#  
#  2017 Keaton Brown <linux.keaton@gmail.com>
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
########################################################################
#
#   Reddit Secret Santa Bot
#
#   Originally designed for /r/ClosetSanta, this bot is intended to
#   handle semi-anonymous messaging for Secret Santa-style events on
#   Reddit. 
#
########################################################################

version = "0.9.0"

print("Reddit Secret Santa Bot (v.{}) initializing.".format(version))

from sys import argv
args = set(arg for arg in argv)
if "-h" in args or "--help" in args:
    exit("--reset          Regenerates santa list from santaList.csv")
import praw, pickle, csv
from sys import path as importpath
from os import path, mkdir
from time import sleep,time,strftime
from urllib.parse import quote
from textwrap import wrap
MYDIR = path.dirname(path.realpath(__file__))
importpath.append(path.join(MYDIR,'Modules'))
import secret

def printbox(s,width=40,ignore=False):
    print('*'*width)
    print(strftime("%D %X"))
    if not ignore:
        print("\n".join(wrap(s,width=width)))
    else:
        print(s)

printbox("Modules imported sucessfully.")
msgArc = path.join(MYDIR,"MessageArchive")
if not path.exists(msgArc):
    mkdir(msgArc)
import PMs
printbox("Initialization successful. Entering main loop.")

while True:
    start = time()
    try:
        PMs.check()
    except Exception as e:
        printbox("Error: "+str(e.args))
    if secret.sleepTime > 0:
        while time() - start < secret.sleepTime:
            sleep(1)
    else:
        exit()