#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Undead
===========

Dead Easy UNIX Daemons!

"""

class Undead(object):
    """ This is the Undead module """


    def __init__(self, name=None, log_level='WARNING',
                 log_handler=None, proc_title = None, **kwargs):

        self.settings = {
            'chroot_directory': None,
            'working_directory': u'/',
            'umask': 0,
            'uid': None,
            'gid': None,
            'prevent_core': True,
            'detach_process': None,
            'files_preserve': None,
            'pidfile': None,
            'stdin': None,
            'stdout': None,
            'stderr': None,
            'signal_map': None,
        }
        self.settings.update(kwargs)

        self.name = name
        self.log_level = log_level
        self.log_handler = log_handler


        def __getattr__(self, name):
            if name in self.settings:
                return self.settings[name]
            else:
                raise AttributeError
        self.__getattr__ = __getattr__

        def __setattr__(self, name, value):
            if name in self.settings:
                self.settings[name] = value
            else:
                self.__dict__[name] = value
        self.__setattr__ = __setattr__

    @property
    def working_dir(self):
        import warnings
        warnings.warn("Deprecated, please use working_directory instead.",
            DeprecationWarning, stacklevel=2)
        return self.settings['working_directory']

    @working_dir.setter
    def working(self, value):
        self.settings['working_directory'] = value

    @property
    def pid(self):
        return self.settings['pidfile']

    @pid.setter
    def pid(self, value):
        import warnings
        warnings.warn("Deprecated, please use pidfile instead.",
            DeprecationWarning, stacklevel=2)
        self.settings['pidfile'] = value

    def __call__(self, action, *args, **kwargs):
        """ Alias for start """
        return self.start(action)

    def start(self, action):
        import os
        import inspect
        import daemon
        import lockfile
        import logbook
        from setproctitle import setproctitle

        self.name = self.name or action.__name__
        default_dir = os.path.join(os.path.expanduser("~"),
                                ".{0}".format(self.name))
        if self.settings['pidfile'] is None:
            self.settings['pidfile'] = os.path.join(default_dir, "{0}.pid".format(self.name))
            if not os.path.exists(default_dir):
                os.makedirs(default_dir)
        if isinstance(self.settings['pidfile'], basestring):
            pid = str(os.getpid())
            with open(self.settings['pidfile'], 'w') as pidfile:
                pidfile.write(pid)
            self.settings['pidfile'] = lockfile.FileLock(self.settings['pidfile'])
        if isinstance(self.proctitle, basestring):
            setproctitle(self.proctitle)
        # Initialize logging if requested.
        action_args = inspect.getargspec(action)[0]
        if 'log' in action_args:
            self.log = logbook.Logger(self.name)

            if self.log_handler is None:
                if not os.path.exists(default_dir):
                    os.makedirs(default_dir)
                self.log_handler = logbook.FileHandler(
                    os.path.join(default_dir, "{0}.log".format(self.name)))
                if self.settings['files_preserve'] is None:
                    self.settings['files_preserve'] = [self.log_handler.stream]
                else:
                    self.settings['files_preserve'].append(self.log_handler.stream)
            self.log_handler.level_name = self.log_level
            with self.log_handler.applicationbound():
                self.log.warning("Starting daemon.")
                with daemon.DaemonContext(**self.settings):
                    action(log=self.log)
        else:
            with daemon.DaemonContext(**self.settings):
                action()


undead = Undead()
import sys
sys.modules[__name__] = undead
# Removing from module ns
del sys
