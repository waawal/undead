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


    def __init__(self):
        self.name = None
        self.log_level = "WARNING" # make a property, accept strings and numbers
        self.log_handler = None # Check for basestring

        class Settings(object):
            def __init__(self):
                self.chroot_directory = None
                self.working_directory = u'/'
                self.umask = 0
                self.uid = None
                self.gid = None
                self.prevent_core = True
                self.detach_process = None
                self.files_preserve = None
                self.pidfile = None
                self.stdin = None
                self.stdout = None
                self.stderr = None
                self.signal_map = None

        self.settings = Settings()

    @property
    def working_dir(self):
        return self.settings.working_directory

    @working_dir.setter
    def my_attr(self, value):
        self.settings.working_directory = value

    @property
    def pid(self):
        return self.settings.pidfile

    @pid.setter
    def my_attr(self, value):
        self.settings.pidfile = value

    def __call__(self, action, *args, **kwargs):
        """ Alias for start """
        self.start = self.start(action)

    def start(self, action):
        import daemon
        from lockfile import FileLock

        self.name = self.name or action.__name__
        default_dir = os.path.join(os.path.expanduser("~"),
                                ".{0}".format(self.name))
        if self.settings.pidfile is None:
            if not os.path.exists(default_dir):
                os.makedirs(default_dir)
            self.settings.pidfile = os.path.join(default_dir, "{0}.pid".format(self.name))

        # Initializing daemon.
        context = daemon.DaemonContext(**self.settings.__dict__)
        # Initialize logging if requested.
        action_args = inspect.getargspec(self.action)[0]
        if 'log' in action_args:
            self.log = logger.Logger(self.name)

            if self.log_handler is None:
            if not os.path.exists(default_dir):
                    os.makedirs(default_dir)
            self.log_handler = logbook.FileHandler(
                os.path.join(default_dir, "{0}.log".format(self.name)))
            if self.settings.files_preserve is None:
                self.settings.files_preserve = [self.log_handler.stream]
            else:
                self.settings.files_preserve.append(self.log_handler.stream)
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
