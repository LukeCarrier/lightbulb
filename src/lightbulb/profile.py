#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

import sys

import lightbulb.applications as applications
import lightbulb.constants as constants


try:
    import yaml
except ImportError:
    print(constants.EXITMESSAGE_MISSINGMODULE
      %("PyYAML", "http://pyyaml.org/wiki/PyYAML"))
    sys.exit(constants.EXITSTATUS_MISSINGMODULE)

def load_file(path):
    """
    Get the contents of a file and parse it into a Profile object.

    This is only here because Luke's lazy and doesn't like closing file
    descriptors.
    """

    with open(path) as file:
        string = file.read()

    return load_string(string)

def load_string(string):
    """
    Parse a string into a Profile object.
    """

    return load_dict(yaml.load(string))

def load_dict(dict):
    """
    Parse a dictionary into a Profile object.
    """

    return Profile(dict)

class Profile:
    """
    Object representation of a profile file.

    This class is effectively used as a datastore, holding all metadata and
    build information collected from a profile's dictionary. Verification of
    the profile's key components also takes place here.
    """

    raw = {}

    name = ""
    description = ""

    components = []

    def __init__(self, dict):
        """
        Initialise a profile object.
        """

        self.raw = dict
        self._init_meta()
        self._init_component_profiles()
        self._catch_unidentified()

    def __str__(self):
        """
        Return a "pretty" string representation of ourself.
        """

        # Is this really necessary?
        #   My understanding is that str.join() should implicitly call str() on
        #   all non-string objects in a sequence, but this doesn't seem to be
        #   the case. For now, this Very Ugly Thing seems to fix it.
        str_repr = "\n\n".join(str(c) for c in self.components)

        return "Profile: %s\nDescription: %s\n\n%s" %(
          self.name, self.description, str_repr)

    def _init_meta(self):
        """
        Initialise profile metadata.

        Verify that the metadata keys exist within the profile dictionary and
        set the relevant values within the profile.
        """

        self.name = self.raw["metadata"]["name"]
        self.description = self.raw["metadata"]["description"]

    def _init_component_profiles(self):
        """
        Initialise profile component information.

        Here, we prepare the data structures used by the build action. This is
        done by simply iterating over the components branch, calling on the
        relevant building block for the given component to parse the options.
        """

        for rc in self.raw["components"]:
            self.components.append(self._init_single_component_profile(rc))

    def _init_single_component_profile(self, raw_component):
        """
        Initialise a single component's data structure.

        This is a helper method for _init_component_profiles().

        Here, we magically translate a dictionary object generated by PyYAML
        (in turn translated from the raw YAML within the profile file) into a
        component configuration object. This involves calling out to each
        component's application module.
        """

        component = getattr(applications, raw_component["application"])
        return component.ComponentProfile(raw_component)

    def _catch_unidentified(self):
        """
        Catch any parameters which haven't yet been handled.

        This is here for deprecation and handling of any unknown parameters.
        Doing this here makes it several times less likely that we'll fuck up
        the machine later.

        @todo actually verify things
        """

        del(self.raw)
