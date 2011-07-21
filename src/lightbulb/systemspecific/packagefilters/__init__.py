#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

import lightbulb.exceptions as exceptions
import lightbulb.systemspecific as systemspecific

def _init_pkg_filter():
    """
    """

    if systemspecific.os_name == "Red Hat Linux":
        mod_name = "redhatenterpriselinux"
    else:
        raise exceptions.UnsupportedOperatingSystemError()

    mod_name = "lightbulb.systemspecific.packagefilters.%s" %(mod_name)
    mod = __import__(mod_name, fromlist = ["package_filter"])
    return getattr(mod, "package_filter")

pkg_filter = _init_pkg_filter()
