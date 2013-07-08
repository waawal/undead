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

    name = None
    pid = None
    log_level = "WARNING"
    file_descriptors = []

    class Daemon(Daemonize):
        """ Subclass of Daemonize to override some methods """


        def __init__(self, action, pid, file_descriptors, name, log_level):
            from logbook import SyslogHandler
            
            self.action = action
            self.name = name or action.__name__
            self.pid = pid
            if self.pid is None:
                self.pid = '/tmp/{0}.pid'.format(self.name)
            self.keep_fds = file_descriptors
            # Initialize logging.
            self.logger = SyslogHandler(self.name, level=log_level)


    def __call__(self, action, *args, **kwargs):
        return self.daemonize(action, *args, **kwargs)

    def daemonize(self, action, *args, **kwargs):
        self.daemon = self.Daemon(action, self.pid, self.file_descriptors,
                             self.name, self.log_level
                             )
        self.daemon.start()
        self.start = self.daemon.start
        self.stop = self.daemon.stop
        self.restart = self.daemon.restart


sys.modules[__name__] = Geist()
# Removing from module ns
del sys
del Daemonize