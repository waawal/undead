#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Undead
===========

Dead Easy UNIX Daemons!

"""

import daemon

class Undead(object):
    """ This is the Undead module """
    import logbook


    name = None
    pid = None
    working_dir = "/"
    log = True
    log_level = "WARNING"
    log_handler = None


    def __call__(self, action, *args, **kwargs):
        """ Alias for start """
        self.start = self.start(action)

    def start(self, action):
        from lockfile import FileLock
        
        home = os.path.join(os.path.expanduser("~"),
                                ".{0}".format(self.name)
                                )
        
        self.lock = FileLock(self.pid)
        if self.lock.is_locked():
            sys.stderr.write("Error: {0} is locked.\n".format(self.pid))
            sys.exit(0)
        with open(self.pid, "w") as lockfile:
            lockfile.write("{0}".format(os.getpid()))
        self.lock.acquire()
        
        # Initialize logging.
        self.log = logger.Logger(self.name)

        if self.log_handler is None:
            if not os.path.exists(home):
                    os.makedirs(home)
            self.log_handler = logbook.FileHandler(
                os.path.join(home, "{0}.log".format(self.name)))
        self.log_handler.level_name = self.log_level
        with self.log_handler.applicationbound():

            # Set custom action on SIGTERM.
            signal.signal(signal.SIGTERM, self._sigterm)
            atexit.register(self._sigterm)

            self.log.warning("Starting daemon.")

            args = inspect.getargspec(self.action)[0]
            if 'log' not in args:
                return self.action()
            self.action(log=self.log)


undead = Undead()
import sys
sys.modules[__name__] = undead
# Removing from module ns
del sys

