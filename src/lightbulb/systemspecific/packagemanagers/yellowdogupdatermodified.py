#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb
#

import sys

import lightbulb.constants as constants
import lightbulb.exceptions as exceptions
from lightbulb.systemspecific import exec_elevated

class PackageManager:
    """
    Yellow Dog Updater Modified (yum) package manager interface.

    This class is used as an interface to yum, the RHEL package management
    utility.

    Due to the fact we only support Python 3.x, this class will simply act as a
    wrapper for the system's yum launcher until the underlying libraries are
    updated (if I know Red Hat at all, this will be in a *long* time).
    """

    _yum_launcher = ""

    def __init__(self):
        """
        Perform initialisation.
        """

        self._find_yum()

    def _find_yum(self):
        """
        @todo make this useful
        """

        self._yum_launcher = "/usr/bin/yum"

    def _exec_cmd(self, action, args):
        """
        """

        args.insert(0, action)
        args.insert(0, "-y")
        args.insert(0, self._yum_launcher)

        try:
            proc = exec_elevated(args)
            status = proc.wait()

            if status > 0:
                raise exceptions.ElevatedApplicationError()
        except exceptions.ElevatedApplicationError:
            print(constants.EXITMESSAGE_PACKAGEMANAGER)
            sys.exit(constants.EXITSTATUS_PACKAGEMANAGER)
        except KeyboardInterrupt:
            print(constants.MESSAGE_CANNOT_INTERRUPT)
            proc.wait()

    def install_pkgs(self, *pkgs):
        """
        Install a list of packages.
        """

        if len(pkgs) == 1 and isinstance(pkgs, (list, tuple)):
            pkgs = pkgs[0]

        pkgs = list(pkgs)

        self._exec_cmd("install", pkgs)
