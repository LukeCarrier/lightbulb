#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

from sys import stdout
import urllib.request

class Download:
    """
    """

    def download(source, target,
      chunk_callback = None,
      chunk_size = 4096):
        """
        Download a file.
        """

        file     = urllib.request.urlopen(source)
        chunk_id = 0

        # We have to set this here because otherwise we'll get a NameError,
        # since the Download class won't be defined. I have no idea why this is,
        # but it seems to work this way.
        if chunk_callback == None:
            chunk_callback = Download._default_download_chunk_callback

        while True:

            chunk = file.read(chunk_size)
            if not chunk:
                break

            target.write(chunk)

            chunk_callback(chunk_id, chunk_size)
            chunk_id += 1

    def _default_download_chunk_callback(chunk_id, chunk_size):
        """
        Default per-chunk download callback.

        This method will output a full-stop (.) on every downloaded chunk. This
        "dotter" is useful for assuring the user that something is happening in
        the background and that the application hasn't just died.
        """

        print(".", end = "")

        # We do an explicit flush of the stdout buffer to ensure that the dot
        # actually gets outputted, since it could be held back for performance
        # reasons otherwise and cause some dodgy output.
        stdout.flush()

