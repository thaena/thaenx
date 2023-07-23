import urllib, datetime, requests, re, os, config
from urllib.request import Request, urlopen
from datetime import datetime
from os import system

# Terminal title
system("title " + "thaenx")

now = datetime.now() # timestamps for console
current_time = now.strftime("%I:%M:%S %p")

broadcasts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'broadcasts.txt') # path to broadcasts.txt

livestreamPage = urllib.request.urlopen(config.yt_channel) # pulls livestream page
livestreamPageBytes = bytes(livestreamPage.read()) # page as bytes
livestreamPageBytes_Decoded = livestreamPageBytes.decode("utf-8") # decodes bytes
livestreamUrl = livestreamPageBytes_Decoded.split('="canonical" href="', 1)[1].split('"', 1)[0] # livestream broadcast url

def notification(): # sents Discord message

    try: # tries to pull scheduled unix time
        scheduledTime = re.search('"scheduledStartTime":"(.+?)",', livestreamPageBytes_Decoded).group(1) # unix time for livestream scheduled

    except: # livestream is live
        payloadData = {"content": ("Stream is now live!\n"+config.messageContent)} # Discord message contents
        headerData = {"authorization": config.token} # Discord message header
        requests.post(config.discord_channel, data=payloadData, headers=headerData) # sends message
        print("["+current_time+"] Notification has been sent, sleeping... ")

    else: # livestream is scheduled
        scheduledTimeDiscordTimestamp = ("<t:"+scheduledTime+">") # unix time in Discord timestamp format
        payloadData = {"content": ("Stream is scheduled to start at "+scheduledTimeDiscordTimestamp+"\n"+config.messageContent)} # Discord message contents
        headerData = {"authorization": config.token} # Discord message header
        requests.post(config.discord_channel, data=payloadData, headers=headerData) # sends message
        print("["+current_time+"] Notification has been sent, sleeping... ")

with open(broadcasts_path, "r+",) as f: # opens broadcasts.txt to read
    contents = f.read() # reads broadcasts.txt

    if contents.find(livestreamUrl) != -1: # searches for URL in broadcasts.txt
        print("["+current_time+"] Stream notification has already been sent, sleeping... ")

    else:
        print("["+current_time+"] Sending stream notification...")
        f.close() # Closes file

        with open(broadcasts_path, "a") as f: # opens broadcasts.txt to append
            f.write("\n"+livestreamUrl) # writes URL in broadcasts.txt
            notification() # sends Discord message
            f.close() # Closes file