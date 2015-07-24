#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy, time, sys, os
import yaml
import logging
import aiml

 
# argfile = str(sys.argv[1])
logger = logging.getLogger(__name__)

# Loading the profiles yaml file to read the informations
# Read config

new_configfile = "/home/pi/.jasper/profile.yml"
logger.debug("Trying to read config file: '%s'", new_configfile)
try:
    with open(new_configfile, "r") as f:
        profile = yaml.safe_load(f)
        #enter the corresponding information from your Twitter application:
        #CONSUMER_KEY = '1234abcd...'#keep the quotes, replace this with your consumer key
        #CONSUMER_SECRET = '1234abcd...'#keep the quotes, replace this with your consumer secret key
        #ACCESS_KEY = '1234abcd...'#keep the quotes, replace this with your access token
        #ACCESS_SECRET = '1234abcd...'#keep the quotes, replace this with your access token secret

        consumer_key = profile['keys']["TW_CONSUMER_KEY"]
        consumer_secret = profile['keys']["TW_CONSUMER_SECRET"]
        access_token = profile['keys']["TW_ACCESS_TOKEN"]
        access_token_secret = profile['keys']["TW_ACCESS_TOKEN_SECRET"]

        print "Authenticating with consumer key %s and consumer secret %s" % (consumer_key, consumer_secret)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        print "Setting access with access token %s and access token secret %s" % (access_token, access_token_secret)
        auth.set_access_token(access_token, access_token_secret)

        print "Authenticating ..."
        api = tweepy.API(auth)
        
        # Load the aiml module
        aimlkernel = aiml.Kernel()

        # Load the aiml files
        folder = "/home/pi/jasper/client/modules/aiml/alice/"
        for file in os.listdir(folder):
            if file.endswith(".aiml"):
                aimlkernel.learn(folder+file)
                print(folder+file)
        folder = "/home/pi/jasper/client/modules/aiml/standard/"
        for file in os.listdir(folder):
            if file.endswith(".aiml"):
                aimlkernel.learn(folder+file)
                print(folder+file)

        # aimlkernel.respond("hi")
        # while True: print aimlkernel.respond(raw_input("> "))
        #  Read the latest direct message
        while True:
            directmessages = api.direct_messages()
            latestdirectmessage = directmessages[0]
            print "Latest direct message %s" % latestdirectmessage.text

            print "Asking the aiml brain for a response"
            aimlresponse = aimlkernel.respond(latestdirectmessage.text)

            print "Tweet back a direct message %s" % aimlresponse
            api.send_direct_message(screen_name = "@t0o1", text = aimlresponse)

            time.sleep(90)

        
        # Post the messages to tweeter
        tweetsfile = "statictweets.txt"
        filename=open(tweetsfile,'r')
        f=filename.readlines()
        filename.close()
         
        for line in f:
            print "Tweeting %s" % line
            #api.update_status(status=line)
            time.sleep(90)#Tweet every 1,5 minutes

except OSError:
    logger.error("Can't open config file: '%s'", new_configfile)
    raise



