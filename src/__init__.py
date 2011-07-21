#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

import argparse
import logging
import logging.handlers
import os
import sys

import lightbulb.actions as actions
import lightbulb.constants as constants
import lightbulb.exceptions as exceptions
import lightbulb.systemspecific as systemspecific

class LightBulb:

    def __init__(self):
        """
        Run LightBulb.
        """

        self._check_os()
        self._init_parser()
        self._init_action()

    def _check_os(self):
        """
        """

        if systemspecific.os_name is None:
            print(constants.EXITMESSAGE_UNSUPPORTEDOS)
            sys.exit(constants.EXITSTATUS_UNSUPPORTEDOS)

    def _init_parser(self):
        """
        Initialise argument parser.

        We depend upon the argparser module to determine which action we should
        be performing. Here, we initialise the argument parser with the various
        different arguments each action group requires.
        """

        # The root parser
        self.parser = argparse.ArgumentParser(
          description     = "LightBulb (LAMP stack compilation tool)",
          epilog          = ("Support is available at %s"
                              %(constants.URL_SUPPORT)),
          prog            = "lightbulb",
        )


        # Subparser factory
        self.subparser_factory = self.parser.add_subparsers(dest = "action")
        self.subparsers = {}

        # Loop through the modules collecting their additional parameters
        #   Check __init__.py in the action package's directory for the other
        #   half of this hack.
        for action in actions.__all__:
            module = getattr(actions, action)
            self.subparsers[action] = module.init_subparser(
              self.subparser_factory.add_parser(action))

        # Parse the arguments
        self.arguments = self.parser.parse_args()

    def _init_action(self):
        """
        Run the action.
        """

        # Run the action by instantiating its class
        getattr(actions, self.arguments.action).Action(self.arguments)

if __name__ == "__main__":
    LightBulb()

