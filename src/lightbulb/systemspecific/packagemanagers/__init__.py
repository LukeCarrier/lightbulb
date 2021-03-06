#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

import lightbulb.exceptions as exceptions
import lightbulb.systemspecific as systemspecific

def _init_pkg_mgr():
    """
    """

    if systemspecific.os_name == "Red Hat Linux":
        mod_name = "yellowdogupdatermodified"
    else:
        raise exceptions.UnsupportedOperatingSystemError()

    mod_name = "lightbulb.systemspecific.packagemanagers.%s" %(mod_name)
    mod = __import__(mod_name, fromlist = ["PackageManager"])
    return getattr(mod, "PackageManager")()

pkg_mgr = _init_pkg_mgr()
