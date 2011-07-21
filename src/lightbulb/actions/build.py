#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

import logging
import os
import shutil
import tempfile
from time import strftime

import lightbulb.applications as applications
import lightbulb.cast as cast
import lightbulb.profile as profile

def init_subparser(subparser):
    """
    Configure the build action argument parser.

    When compiling a stack, we need the path to the profile file as a
    parameter, and possibly some optional extra flags to configure the logging
    system.
    """

    # Path to the profile file
    subparser.add_argument(
      "-p",
      "--profile",
      help     = "build profile",
      dest     = "profile_file",
      required = True
    )

    # Temporary working directory
    subparser.add_argument(
      "-d",
      "--work-dir",
      help    = "working directory",
      nargs   = "?",
      default = None,
      dest    = "work_dir"
    )

    # Automatically delete the build directory
    subparser.add_argument(
      "-e",
      "--erase-work-dir",
      help    = "erase the working directory when the build is complete",
      nargs   = "?",
      default = "true",
      dest    = "erase_work_dir"
    )

    # File feedback level
    subparser.add_argument(
      "-l",
      "--log-level",
      help    = "minimum level of messages to be included in the log",
      nargs   = "?",
      default = "info",
      choices = ["debug", "info", "warning", "error", "critical"],
      dest    = "log_level"
    )

    # Shell feedback level
    subparser.add_argument(
      "-o",
      "--output-level",
      help    = "minimum level of messages to be included in the output",
      nargs   = 1,
      default = "info",
      choices = ["debug", "info", "warning", "error", "critical"],
      dest    = "output_level"
    )

    return subparser

class Action:
    """
    Build action handler.
    """

    def __init__(self, arguments):
        """
        Run LightBulb's build action.
        """

        self.arguments = arguments

        # Do all environment-related configuration here
        self._init_work_dir()
        self._init_logging()

        # ...and then begin the build process
        self._init_profile()
        self._init_build()
        self._init_cleanup()

    def _init_logging(self):
        """
        Initialise logging.

        Logging is used to log any errors encountered during the build process
        any warnings thrown during operations within the application. Here, we
        initialise the logger instance and prepare formatting and such.

        We not only initialise the lightbulb.log interface here, we also
        configure the shell one. This enables messages to be logged to both the
        log file and the shell simultaneously.
        """

        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.DEBUG)

        self.log_format = logging.Formatter(
          fmt     = "[%(asctime)s] [%(levelname)-1s] %(message)s",
          datefmt = "%d/%m/%Y %I:%M:%S"
        )

        self.shell_handler = logging.StreamHandler()
        self.shell_handler.setLevel(getattr(logging,
          self.arguments.output_level.upper()))
        self.shell_handler.setFormatter(self.log_format)
        self.logger.addHandler(self.shell_handler)

        self.log_file = "%s/lightbulb.log" %(self.work_dir)
        self.log_handler = logging.handlers.RotatingFileHandler(
          filename    = self.log_file,
          mode        = "w"
        )
        self.log_handler.setLevel(getattr(logging,
          self.arguments.log_level.upper()))
        self.log_handler.setFormatter(self.log_format)
        self.logger.addHandler(self.log_handler)

        self.logger.info("Now logging to %s" %(self.log_file))

    def _init_work_dir(self):
        """
        """

        # Determine the name of the log from the profile
        #   Put simply, discard anything before and including the final "/", and
        #   do the same with anything after and including the final ".". There's
        #   almost certainly a better way of doing this, but it works!
        if not self.arguments.work_dir:
            self.arguments.work_dir = "_%s_%s" %(
              "_".join(self.arguments.profile_file.split("/")[-1:][0]
                .split(".")[:-1]),
              strftime("%d-%m-%Y_%I-%M-%S")
            )

        self.work_dir = tempfile.mkdtemp(suffix = self.arguments.work_dir)

    def _init_profile(self):
        """
        """

        self.logger.info("Parsing profile")
        self.profile = profile.load_file(self.arguments.profile_file)
        self.logger.info("Interpreted profile as:\n%s" %(self.profile))

    def _init_build(self):
        """
        """

        self.logger.info("Beginning build process")

        app_id = 0

        for ac in self.profile.components:
            app_work_dir = "%s/%s" %(self.work_dir, str(app_id))
            os.mkdir(app_work_dir)
            getattr(applications, ac.application).ComponentBuilder(ac,
              self.logger, app_work_dir)
            app_id += 1

        self.logger.info("Build process complete")

    def _init_cleanup(self):
        """
        Clean up any temporary kludge left behind by the build.

        Whenever LightBulb is executed it, it creates a fair few temporary
        files which are used for logging the actions taken by the application,
        temporarily storing any downloaded source code and actually patching it
        and performing the build. For the sake of simplicity, these all remain
        within the working directory specified on the command line or in a
        directory created by Python's tempfile module - we don't leave junk in
        any system directories.

        If the -e (--erase-work-dir) switch is set to True (or otherwise
        evaluates to such), we remove the aforementioned directory here.
        """

        self.logger.info("Beginning cleanup process")
        if cast.str_to_bool(self.arguments.erase_work_dir):
            self.logger.info("Removing working directory")
            shutil.rmtree(self.work_dir)
        else:
            self.logger.info("Left working directory intact - it will need to "
              + "be removed manually")
        self.logger.info("Cleanup process complete")
