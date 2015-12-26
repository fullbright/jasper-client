# -*- coding: utf-8-*-
import logging
import modules.aiml
from notifier import Notifier
from brain import Brain


class Conversation(object):

    def __init__(self, persona, mic, profile):
        self._logger = logging.getLogger(__name__)
        self.persona = persona
        self.mic = mic
        self.profile = profile
        self.brain = Brain(mic, profile)
        self.notifier = Notifier(profile)
        # Load the aiml module
        self.aimlkernel = aiml.Kernel()

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

    def handleForever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.info("Starting to handle conversation with keyword '%s'.",
                          self.persona)
        while True:
            # Print notifications until empty
            notifications = self.notifier.getAllNotifications()
            for notif in notifications:
                self._logger.info("Received notification: '%s'", str(notif))

            self._logger.debug("Started listening for keyword '%s'",
                               self.persona)
            threshold, transcribed = self.mic.passiveListen(self.persona)
            self._logger.debug("Stopped listening for keyword '%s'",
                               self.persona)

            if not transcribed or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue
            self._logger.info("Keyword '%s' has been said!", self.persona)

            self._logger.debug("Started to listen actively with threshold: %r",
                               threshold)
            input = self.mic.activeListenToAllOptions(threshold)
            self._logger.debug("Stopped to listen actively with threshold: %r",
                               threshold)

            if input:
                self.brain.query(input)
            else:
                self.mic.say("Pardon?")
