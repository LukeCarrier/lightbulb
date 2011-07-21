#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

def str_to_bool(str):
    """
    Cast a string to boolean.
    """

    if str.lower() in ["false", "no", "none", "null"]:
        res = False
    else:
        res = True

    return res
