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

    settings = {
    'chroot_directory': None
    'working_directory': u'/'
    'umask': 0
    'uid': None
    'gid': None
    'prevent_core': True
    'detach_process': None
    'files_preserve': None
    'pidfile': None
    'stdin': None
    'stdout': None
    'stderr': None
    'signal_map': None
    }

    name = None
    log_level = "WARNING"
    log_handler = None # Check for basestring

    #TODO: properties
    @property
    def working_dir(self):
        return settings['working_directory']

    @working_dir.setter
    def my_attr(self, value):
        settings['working_directory'] = value

    @property
    def pid(self):
        return settings['pidfile']

    @pid.setter
    def my_attr(self, value):
        settings['pidfile'] = value

    def __call__(self, action, *args, **kwargs):
        """ Alias for start """
        self.start = self.start(action)

    def start(self, action):
        import daemon
        from lockfile import FileLock
        
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
        # Initializing daemon.
        context = daemon.DaemonContext(**self.settings)
        # Initialize logging.
        action_args = inspect.getargspec(self.action)[0]
        if 'log' in action_args:
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
