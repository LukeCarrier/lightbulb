#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

import lightbulb.constants as constants

class ElevatedApplicationError(Exception):
    """
    """

    pass

class UnsupportedOperatingSystemError(Exception):
    """
    """

    def __str__(self):
        """
        Return a string representation.
        """

        return constants.EXITMESSAGE_UNSUPPORTEDOS

class InvalidApplicationPathError(Exception):
    """
    Invalid application path error.

    We raise this whenever a path that seems unreasonable is specified as part
    of a component definition.
    """

    def __init__(self, application, key, value):
        """
        Initialise error information values.
        """

        self.application = application
        self.key = key
        self.value = value

    def __str__(self):
        """
        Return a string representation.
        """

        return "Invalid path '%s' for key '%s' in application '%s'" %(
          self.value, self.key, self.application)

class ApplicationBuildError(Exception):
    """
    Application build error.

    If an application fails to build for whatever reason, this catch-all
    error should be raised.
    """

    pass

class UnsupportedApplicationVersionError(Exception):
    """
    Unsupported application version error.

    This exception should be thrown whenever the version of an application
    specified as a build component isn't supported by its application module
    (usually because its upstream vendor has dropped support for it).
    """

    def __init__(self, application, version):
        """
        Initialise error information values.
        """

        self.application = application
        self.version = version

    def __str__(self):
        """
        Return a string representation.
        """

        return "Unsupported version '%s' of application '%s'" %(
          self.version, self.application)
