#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

import os
import subprocess

from lightbulb.config import permission_elevation
import lightbulb.exceptions as exceptions

def exec_elevated(args, **etc):
    """
    Run an application as an administrative user.

    Run the application specified in args[0] as the system's root user, or
    equivalent. Currently, this requires the use of Elevator, configured with
    the allow gid/uid of the user you're running LightBulb as.
    """

    if permission_elevation["method"] == "elevator":
        args.insert(0, permission_elevation["elevator"])
    else:
        raise exceptions.ElevatedApplicationError()

    etc["bufsize"] = 1
    etc["stdin"]   = None

    return subprocess.Popen(args, **etc)

def which(util, path = None):
    """
    Find a system utility.
    """

    if not path:
        path = os.environ["PATH"]

    paths = path.split(":")

    for path in paths:
        if os.path.isfile("%s/%s" %(path, util)):
            return "%s/%s" %(path, util)

    return None

def _os_name():
    """
    Get OS information.

    Evil! Probably unreliable too! Still, we need this so we know which package
    manager to use to pull dependencies. THE USE OF THIS FUNCTION FOR ANY OTHER
    PURPOSE IS PROBABLY A BAD ONE!
    """

    if os.name == "posix" and os.path.isfile("/etc/redhat-release"):
        os_name = "Red Hat Linux"
    else:
        os_name = None

    return os_name

os_name = _os_name()
