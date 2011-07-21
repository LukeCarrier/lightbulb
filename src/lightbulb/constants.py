#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

# Version constants
#   These might be used by future modules to ensure compatibility, or
#   something along those lines.
VERSION_STRING = "0.0.1"
VERSION_LIST = VERSION_STRING.split(".")

# Support URL
#   This is displayed in help messages and such. I might add more URLs as
#   time goes on, but this is mostly here just so I can change them easily,
#   just in case. ;)
URL_SUPPORT = "http://github.com/cloudflux/lightbulb"

# Missing module error format string
#   The string we'll print right before we implode on ourselves. We substitute
#   in the package name and the home or download page URL respectively.
EXITMESSAGE_MISSINGMODULE = ( "%s is required by this application and could "
                            + "not be imported. You can install it via "
                            + "distribute or easy_install, or download it from "
                            + "%s")

# Missing module exit status
#   We throw this exit status when we fail to locate a library critical to the
#   application's execution - it should contain the same value as "EX_OSFILE" in
#   sysexits.h (part of libc).
EXITSTATUS_MISSINGMODULE = 72

# Unsupported OS exit message
#   This message will be printed right before the application exits because it
#   doesn't have support for the OS it's running under (missing package manager
#   module, etc.).
EXITMESSAGE_UNSUPPORTEDOS = ( "It appears as though LightBulb doesn't "
                            + "currently support your operating system. "
                            + "Because of its low-level nature, LightBulb "
                            + "needs special libraries to interface with your "
                            + "system's package management utility and to "
                            + "determine which dependencies it should install."
                            + "\n\nIf you believe we made a mistake and your "
                            + "OS is supported (or you would like it to be), "
                            + "please file a ticket at %s" %(URL_SUPPORT))

# Unsupported OS exit status
EXITSTATUS_UNSUPPORTEDOS = 72

EXITMESSAGE_PACKAGEMANAGER = ( "LightBulb attempted to use the system package "
                             + "manager, but it appears as though it ran into "
                             + "issues when processing our command.\n\nThis "
                             + "may be an issue with your system's "
                             + "configuration or it could be a bug in "
                             + "LightBulb. For help troubleshooting, please "
                             + "post your \"lightbulb.log\" file for this "
                             + "build at %s"
                             %(URL_SUPPORT))

# Package manager error exit status.
EXITSTATUS_PACKAGEMANAGER = 70

EXITMESSAGE_INTERRUPTED = ( "LightBulb was interrupted while working and has "
                          + "been aborted. This usually happens because of a "
                          + "keybord interrupt (CTRL + C) and is not good "
                          + "practice, as it can cause major damage to system "
                          + "files and caches.")

EXITSTATUS_INTERRUPTED = 64

MESSAGE_CANNOT_INTERRUPT = ( "Because of the low-level nature of the work "
                           + "LightBulb is currently performing, the process "
                           + "cannot abort at this time. Please be patient, "
                           + "as the application will exit at the next "
                           + "available opportunity.")
