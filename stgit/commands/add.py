
__copyright__ = """
Copyright (C) 2005, Catalin Marinas <catalin.marinas@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

import sys, os
from optparse import OptionParser, make_option

from stgit.commands.common import *
from stgit.utils import *
from stgit import stack, git


help = 'add files or directories to the repository'
usage = """%prog [options] <files/dirs...>

Add the files or directories passed as arguments to the
repository. When a directory name is given, all the files and
subdirectories are recursively added."""

directory = DirectoryHasRepository(needs_current_series = False)
options = []


def func(parser, options, args):
    """Add files or directories to the repository
    """
    if len(args) < 1:
        parser.error('incorrect number of arguments')

    git.add(args)
