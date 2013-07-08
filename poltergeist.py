#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Poltergeist
===========

Dead Easy UNIX Daemons!

"""

import sys

from daemonize import Daemonize
__all__ = __name__


class Geist(object):
    """ This is the Poltergeist module """


    class Daemon(Daemonize):
        """ Subclass of Daemonize to override some methods """


        def __init__(self):
            pass


    def __call__(self, action, *args, **kwargs):
        return self.daemonize(action, *args, **kwargs)

    def daemonize(self, action, *args, **kwargs):
        print action
        print args
        action()

sys.modules[__name__] = Geist()
# Removing from module ns
del sys
del Daemonize