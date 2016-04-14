# -*- coding: utf-8-*-
import logging
import pkgutil
import jasperpath
from owyl import blackboard
import owyl


class BehaviourTree(object):

    def __init__(self):
        """
        Instantiates a new Brain object, which cross-references user
        input with a list of modules. Note that the order of brain.modules
        matters, as the Brain will cease execution on the first module
        that accepts a given input.

        Arguments:
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        """
        self.bb = blackboard.Blackboard("jasperbrain")
        #self.schedule(self.update)
        self.behaviour = self.buildTree()
        self._logger = logging.getLogger(__name__)

    def buildTree(self):
        """ Build the behaviour buildTree
            Building a behaviour tree is as simple as nesting 
            behaviour constructor calls.

            Building the behaviour tree
            ============================

            We use parallel to have many behaviour tree run at the same time
            - check the internet connection
            - check new tweets and reply
            - check for new emails

            Core Behaviours
            ===============

            The core behaviour are documented below in each method's docstring. They are :
            - Brain.query : queries all modules for a response to a question
            - Brain.checkinternet : check that internet connexion is available
            - Brain.checknewtweets : check that new tweets are available.
            - Brain.checknewemails : check that there are new emails


        """

        tree = owyl.parallel(
                    ### Check that internet is available
                    ####################################
                    owyl.limit(
                        owyl.repeatAlways(self.checkinternet(), debug=True), 
                        limit_period=2.4
                    ),

                    ### Check new tweets
                    ####################################
                    self.checknewtweets(),

                    ### Check new emails
                    ####################################
                    self.checknewemails(),

                    policy=owyl.PARALLEL_SUCCESS.REQUIRE_ALL

            )

        return owyl.visit(tree, blackboard=self.bb)

    @owyl.taskmethod
    def checkinternet(self, **kwargs):
        """ Checks that internet is available
        @keyword internet : available or not
        """
        self._logger.debug("Checking for internet availability")
        print("Checking for internet availability")
        #yield True

        while True:
        	print "check check internet ..."
        	yield True

    @owyl.taskmethod
    def checknewtweets(self, **kwargs):
        """
        Check to see if there are new tweets to process
        """
        self._logger.debug("Checking for new tweets")
        print("Checking for new tweets")
        #yield True

        while True:
        	print "check check tweets ..."
        	yield False

    @owyl.taskmethod
    def checknewemails(self, **kwargs):
        """
        Check to see if there are new tweets to process
        """
        self._logger.debug("Checking for new emails")
        print("Checking for new emails")
        #yield True

        while True:
        	print "check check emails ..."
        	yield True

    def update(self, dt):
        """
        Update the behaviour tree.
        This get scheduled in __init__
        @param dt: Change in time since last update
        @type dt: C{float} in seconds

        """
        self.bb['dt'] = dt
        #self.behaviour.next()


    def tick(self):
    	print("** tick **")
        self.behaviour.next()
        #owyl.visit(self.behaviour)

    @classmethod
    def get_modules(cls):
        """
        Dynamically loads all the modules in the modules folder and sorts
        them by the PRIORITY key. If no PRIORITY is defined for a given
        module, a priority of 0 is assumed.
        """

        logger = logging.getLogger(__name__)
        locations = [jasperpath.PLUGIN_PATH]
        logger.debug("Looking for modules in: %s",
                     ', '.join(["'%s'" % location for location in locations]))
        modules = []
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except:
                logger.warning("Skipped module '%s' due to an error.", name,
                               exc_info=True)
            else:
                if hasattr(mod, 'WORDS'):
                    logger.debug("Found module '%s' with words: %r", name,
                                 mod.WORDS)
                    modules.append(mod)
                else:
                    logger.warning("Skipped module '%s' because it misses " +
                                   "the WORDS constant.", name)
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY')
                     else 0, reverse=True)
        return modules

    def query(self, texts):
        """
        Passes user input to the appropriate module, testing it against
        each candidate module's isValid function.

        Arguments:
        text -- user input, typically speech, to be parsed by a module
        """
        for module in self.modules:
            for text in texts:
                if module.isValid(text):
                    self._logger.debug("'%s' is a valid phrase for module " +
                                       "'%s'", text, module.__name__)
                    try:
                        module.handle(text, self.mic, self.profile)
                    except:
                        self._logger.error('Failed to execute module',
                                           exc_info=True)
                        self.mic.say("I'm sorry. I had some trouble with " +
                                     "that operation. Please try again later.")
                    else:
                        self._logger.debug("Handling of phrase '%s' by " +
                                           "module '%s' completed", text,
                                           module.__name__)
                    finally:
                        return
        self._logger.debug("No module was able to handle any of these " +
                           "phrases: %r", texts)

def main():
	print("Starting behaviour tree")
	bt = BehaviourTree()

	print("Starting the loop")
	while True:
		bt.tick()

if __name__ == '__main__':
	main()