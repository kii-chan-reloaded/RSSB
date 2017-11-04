#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  PMs.py
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

from __main__ import *

picklePath = path.join(MYDIR,'Objects')
if not path.exists(picklePath):
    mkdir(picklePath)

santaPath = path.join(picklePath,"santaList.pkl")
if path.exists(santaPath) and not "--reset" in args:
    santaList = pickle.load(open(santaPath,'rb'))
else:
    csvPath = path.join(MYDIR,'santaList.csv')
    if not path.exists(csvPath):
        exit("Error: Santa list not found. Please save an appropriate .csv as "+csvPath)
    santaList = { 'to santa':{}, 'as santa':{} }
    with open(csvPath,'r') as f:
        reader = csv.reader(f)
        header = reader.__next__()
        if len(header) != 2:
            exit("Error: "+csvPath+" is an improper size. It must be two columns (user, user's santa.)")
        for user, santa in reader:
            santaList['to santa'][user.lower()] = santa
            santaList['as santa'][santa.lower()] = user
    pickle.dump(santaList,open(santaPath,'wb'))
print("Santa list read successfully.")

try:
    reddit = praw.Reddit(client_id=secret.client_id,
                        client_secret=secret.client_secret,
                        password=secret.password,
                        user_agent="Reddit Secret Santa Bot, version {v} for /r/{sub}, hosted by /u/{me}".format(
                                    v=version,sub=secret.mySubreddit,me=secret.me),
                        username=secret.username)
except Exception as e:
    exit("Error: Reddit authentication failed. Check for correct credentials and internet connection\n\nMore details: "+str(e.args))
print("Reddit credentials obtained.")

PMLink = "https://www.reddit.com/message/compose/?to={bot}&subject={func}".format(bot=secret.username,func="{func}")
toSantaLink = "[Send a message to your santa]({})".format(PMLink.format(func=quote("To Santa")))
fromSantaLink = "[Send a message to your gift-recipient]({})".format(PMLink.format(func=quote("As Santa")))
printbox("To Santa Link: "+toSantaLink+"\n"+"From Santa Link: "+fromSantaLink,ignore=True)
reportLink = "[report this message]({})".format(PMLink.format(func=quote("Report ")+"{}&message="+quote(
             "Please give the moderators a short reason for the report.")))

preflair = "\n****\nReply to this message to have your reply forwarded. If you feel the need, "+reportLink
botFlair="\n\nHappy holidays!\n*****\n{to} | {fs}\n\n[^^I'm ^^open ^^source!](https://github.com/WolfgangAxel/RSSB)".format(
                                                                                            to=toSantaLink,fs=fromSantaLink)

def check():
    for message in reddit.inbox.unread():
        if message.author.name.lower() not in santaList['to santa']:
            reddit.redditor(message.author.name).message("Delivery Failure","Your username is not in the list of "+
                          "users participating in this exchange. Please [contact the moderators]"+
                          "(https://www.reddit.com/message/compose/?to="+quote("/r/"+secret.mySubreddit,safe='')+
                          ") if you feel there is a mistake."+botFlair)
            message.mark_read()
            continue
        if message.subject.lower() in ("re: delivery receipt","re: delivery failure"):
            message.mark_read()
            continue
        if message.subject.lower() not in ("to santa", "re: a message from your secret santa",
                                          "as santa", "re: a message from your gift recipient") and (
                                          "report " not in message.subject.lower()):
            reddit.redditor(message.author.name).message("Delivery Failure","Your message had an improper title. "+
                                                         "Please use one of the templated links to utilize this bot."+botFlair)
            message.mark_read()
            continue
        if message.subject.lower() in ("to santa", "re: a message from your secret santa"):
            # To santa function
            sendMessage(message.author.name,message.body,'to santa')
        elif message.subject.lower() in ("as santa", "re: a message from your gift recipient"):
            # From santa function
            sendMessage(message.author.name,message.body,'as santa')
        else:
            messageID = message.subject.lower().replace("report ","")
            if path.exists(path.join(msgArc,messageID+".txt")):
                # Report function
                reportMessage(messageID,message.body)
            else:
                message.reply("Your report contained an invalid ID. Please do not alter the title of the report message and try again. "
                              "If the problem persists, [contact the moderators](https://www.reddit.com/message/compose/?to="+
                              quote("/r/"+secret.mySubreddit,safe='')+")"+botFlair)
                message.mark_read()
                continue
        reddit.redditor(message.author.name).message("Delivery Receipt","Your message was successfully delivered!"+botFlair)
        message.mark_read()

def saveMessage(name,to,msg,msgID):
    with open(path.join(msgArc,msgID+".txt"),"w") as f:
        f.write(strftime("%D %X")+"\nMessage from /u/{name} to /u/{to}\n****\n".format(name=name,to=to)+msg)

def sendMessage(name,body,direction):
    if direction == "to santa":
        title = "A Message from your Gift Recipient"
        greeting = "Hello, /u/{user}!\n\nYou have received a message from your gift recipient:\n****\n".format(
                                                                        user=santaList[direction][name.lower()])
    else:
        title = "A Message from your Secret Santa"
        greeting = "Hello, /u/{user}!\n\nYou have received a message from your Secret Santa:\n****\n".format(
                                                                        user=santaList[direction][name.lower()])
    messageID = strftime("%y.%m.%d.%H.%M.%S.")+str(time() % 1)[2:4]
    wholeMessage = greeting+body+preflair.format(messageID)+botFlair
    saveMessage(name,santaList[direction][name.lower()],body,messageID)
    if len(wholeMessage) < 10000:
        reddit.redditor(santaList[direction][name.lower()]).message(title,wholeMessage)
    else:
        bits = wrap(wholeMessage,width=9000,drop_whitespace=False,replace_whitespace=False)
        for i,part in enumerate(bits):
            reddit.redditor(santaList[direction][name.lower()]).message(title,"({n}/{d})\n\n".format(n=i+1,d=len(bits))+part)

def reportMessage(msgID,reason):
    with open(path.join(msgArc,msgID+".txt"),'r') as f:
        reported = f.read()
    if len(reason) > 1000:
        reason = reason[:1000]+"... (reason was too long. PM the afflicted party for more information)"
    if len(reason+"\n****\n"+reported) < 10000:
        reddit.subreddit(secret.mySubreddit).message('Reported interaction - '+path.join('MessageArchive',msgID),reason+"\n****\n"+reported)
    else:
        fluff = len(reason+"\n****\n"+" (__/__)")
        bits = wrap(reported,width=10000-fluff,drop_whitespace=False,replace_whitespace=False)
        for i,part in enumerate(bits):
            reddit.subreddit(secret.mySubreddit).message('Reported interaction - '+path.join('MessageArchive',msgID),
                                                         reason+" ({n}/{d})\n****\n".format(n=i+1,d=len(bits))+part)
