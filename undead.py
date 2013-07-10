#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Undead
===========

Dead Easy UNIX Daemons!

"""

class Undead(object):
    """ This is the Undead module """
    import logbook


    name = None
    pid = None
    working_dir = "/"
    log_level = "WARNING"
    log_handler = None


    def __call__(self, action, *args, **kwargs):
        """ Alias for start """
        self.start = self.start(action)

    def start(self, action):
        import daemon
        from lockfile import FileLock
        context = daemon.DaemonContext()
        
        default_dir = os.path.join(os.path.expanduser("~"),
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
        args = inspect.getargspec(self.action)[0]
        if 'log' in args:
            self.log = logger.Logger(self.name) # Todo: add fh to open files

            if self.log_handler is None:
            if not os.path.exists(default_dir):
                    os.makedirs(default_dir)
            self.log_handler = logbook.FileHandler(
                os.path.join(default_dir, "{0}.log".format(self.name)))
            self.log_handler.level_name = self.log_level
            with self.log_handler.applicationbound():
                self.log.warning("Starting daemon.")
                with context:
                    self.action(log=self.log)
        else:
            with context:
                self.action()


undead = Undead()
import sys
sys.modules[__name__] = undead
# Removing from module ns
del sys
