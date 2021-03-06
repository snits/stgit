# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import email
import os
import sys

# With unicode_literals enabled, the type of a string literal will be `unicode`
# for Python 2 and `str` for Python 3.
text = type('')

# PEP-540 (Add a new UTF-8 mode) makes a compelling argument for Python
# programs making special effort to work around misconfigured locale
# settings. This largely boils down to treating incoming byte sequences,
# i.e. command line arguments and environment variables, as UTF-8.
#
# This is specifically relevant when the POSIX (aka C) locale is in effect.
#
# https://www.python.org/dev/peps/pep-0540/
#
# The following functions help achieve this goal by using UTF-8 as a fallback
# encoding when the nominal encoding (sys.getfilesystemencoding()) fails.
if sys.version_info[0] <= 2:
    _fs_enc = sys.getfilesystemencoding()

    def fsdecode_utf8(b):
        """Decode to filesystem encoding, with UTF-8 fallback."""
        if isinstance(b, bytes):
            try:
                return b.decode(_fs_enc)
            except UnicodeDecodeError:
                return b.decode('utf-8')
        else:
            return fsdecode_utf8(fsencode_utf8(b))

    def fsencode_utf8(s):
        """Encode to filesystem encoding, with UTF-8 fallback."""
        try:
            return s.encode(_fs_enc)
        except UnicodeEncodeError:
            return s.encode('utf-8')
else:  # Python 3
    def fsdecode_utf8(b):
        if isinstance(b, bytes):
            try:
                return os.fsdecode(b)
            except UnicodeDecodeError:
                return b.decode('utf-8')
        else:
            return os.fsencode(b).decode('utf-8')

    def fsencode_utf8(s):
        try:
            return os.fsencode(s)
        except UnicodeEncodeError:
            return s.encode('utf-8')


class file_wrapper(object):
    """Wrap file object with missing methods needed by TextIOWrapper."""

    def __init__(self, f, readable=False, writable=False, seekable=False):
        self.__f = f
        self.__readable = readable
        self.__writable = writable
        self.__seekable = seekable

    def __getattr__(self, name):
        return getattr(self.__f, name)

    def readable(self):
        return self.__readable

    def writable(self):
        return self.__writable

    def seekable(self):
        return self.__seekable


# Python 2 only has email.message_from_file(), but it behaves like Python 3's
# email.message_from_binary_file().
message_from_binary_file = getattr(email, 'message_from_binary_file',
                                   email.message_from_file)
