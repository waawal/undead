#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Poltergeist
===========

Dead Easy UNIX Daemons!

"""

class Geist(object):
    """ This is the Poltergeist module """


    name = None
    pid = None
    log_level = "WARNING"
    file_descriptors = []

    
    def __call__(self, action, *args, **kwargs):
        return self.daemonize(action, *args, **kwargs)

    def daemonize(self, action, *args, **kwargs):
        self.daemon = self.start(action, self.pid, self.file_descriptors,
                             self.name, self.log_level
                             )
        self.daemon.start()

    def start(self, action, pid, file_descriptors, name, log_level):
        import fcntl
        import os
        import sys
        import signal
        import resource
        import atexit
        import inspect

        from logbook import SyslogHandler
        
        self.action = action
        self.name = name or action.__name__
        self.pid = pid
        if self.pid is None:
            self.pid = '/tmp/{0}.pid'.format(self.name)
        self.file_descriptors = file_descriptors
        # Initialize logging.
        self.logger = SyslogHandler(self.name, level=log_level)

        process_id = os.fork()
        if process_id < 0:
            sys.exit(1)
        elif process_id is not 0:
            sys.exit(0)
        process_id = os.setsid()
        if process_id is -1:
            sys.exit(1)
        devnull = "/dev/null"
        if hasattr(os, "devnull"):
            devnull = os.devnull

        for fd in range(resource.getrlimit(resource.RLIMIT_NOFILE)[0]):
            if fd not in self.file_descriptors:
                try:
                    os.close(fd)
                except OSError:
                    pass

        os.open(devnull, os.O_RDWR)
        os.dup(0)
        os.dup(0)

        os.umask(0o27)
        os.chdir("/")

        lockfile = open(self.pid, "w")
        fcntl.lockf(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)

        lockfile.write("{0}".format(os.getpid()))
        lockfile.flush()

        # Set custom action on SIGTERM.
        signal.signal(signal.SIGTERM, self.sigterm)
        atexit.register(self.sigterm)

        self.logger.warn("Starting daemon.")

        args = inspect.getargspec(self.action)[0]
        if 'logger' not in args:
            return self.action()
        self.action(logger=self.logger)

    def sigterm(self, signum=None, frame=None):
        if signum is None:
            self.logger.warn("Stopping daemon.")
        else:
            self.logger.warn("Signal: {0} - Stopping daemon.".format(signum))
        os.remove(self.pid)
        sys.exit(0)

geist = Geist()
import sys
sys.modules[__name__] = geist
# Removing from module ns
del sys