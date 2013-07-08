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
    log_handler = None


    def __call__(self, action, *args, **kwargs):
        """ Alias for start """
        self.start = self.start(action)

    def start(self, action):
        """ Does the daemon dance """
        import fcntl
        import os
        import sys
        import signal
        import resource
        import atexit
        import inspect

        from logbook import Logger, FileHandler
        
        self.action = action
        self.name = self.name or action.__name__

        home = os.path.join(os.path.expanduser("~"),
                                ".{0}".format(self.name)
                                )
        if self.pid is None:
            if not os.path.exists(home):
                os.makedirs(home)
            self.pid = os.path.join(home, "{0}.pid".format(self.name))
        # Initialize logging.
        self.log = Logger(self.name)

        if self.log_handler is None:
            if not os.path.exists(home):
                    os.makedirs(home)
        self.log_handler = FileHandler(
            os.path.join(home, "{0}.log".format(self.name)),
            level=self.log_level
            )
        with self.log_handler.applicationbound():
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

            os.open(devnull, os.O_RDWR)
            os.dup(0)
            os.dup(0)

            os.umask(0o27)
            os.chdir("/")

            try:
                lockfile = open(self.pid, "w")
                fcntl.lockf(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                sys.stderr.write("Error: {0} is locked.".format(self.pid))
                sys.exit(1)
            lockfile.write("{0}".format(os.getpid()))
            lockfile.flush()
            # Set custom action on SIGTERM.
            signal.signal(signal.SIGTERM, self._sigterm)
            atexit.register(self._sigterm)

            self.log.warning("Starting daemon.")

            args = inspect.getargspec(self.action)[0]
            if 'log' not in args:
                return self.action()
            self.action(log=self.log)

    def _sigterm(self, signum=None, frame=None):
        import os
        import sys
        with self.log_handler.applicationbound():
            if not signum:
                self.log.warning("Stopping daemon.")
            else:
                self.log.warning("Signal: {0} -Stopping daemon.".format(signum))
            try:
                os.remove(self.pid)
            except OSError:
                pass
            finally:
                sys.exit(0)

geist = Geist()
import sys
sys.modules[__name__] = geist
# Removing from module ns
del sys