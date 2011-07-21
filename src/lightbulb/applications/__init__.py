#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

import pkgutil

# Make submodules accessible
#   This is fairly dirty, but it does work. We need to load all submodules here
#   so that they're accessible to anything that imports this package can access
#   them. Sadly, there's no nice alternative to dir() for packages. and __all__
#   only represents submodules that have already been loaded.
__all__ = []
for (loader, module_name, is_package) in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    module = loader.find_module(module_name).load_module(module_name)
    exec("%s = module" %(module_name))
