undead
======

Dead Easy POSIX Daemons for Python!

-------------------------------------------------------------------------

.. code:: python

    #!/usr/bin/python
    import undead

    @undead
    def my_daemon_process():
        """ This function will be daemonized. """
        from time import sleep
        while True:
            sleep(10)

-------------------------------------------------------------------------

Settings
--------

undead.name
  Name of the logger.

  Default: ``__name__`` of decorated callable

undead.pid
  Path to logfile.  

  Default: ``~/.{undead.name}/{undead.name}.pid``

undead.working_dir
  Path to working directory.  

  Default: ``"/"``

undead.log_level
  Log level.  

  Default: ``"WARNING"``

undead.log_handler
  The logbook handler.

  Default: ``~/.{undead.name}/{undead.name}.log``

Example
*******

.. code:: python

    import undead
    from logbook import SyslogHandler

    undead.name = "Tangina Barrons"
    undead.pid = "/var/log/tangina.pid"
    undead.working_dir = "/var/www"
    undead.log_level = "ERROR"
    undead.log_handler = SyslogHandler("My Daemon", level="ERROR")

    @undead
    def my_daemon_process():
        """ This function will be daemonized. """
        # ...

Logging within the decorated handler
------------------------------------

Just add ``log`` to your decorated signature, and the logger will be passed down. Log away captain!

.. code:: python

    import undead

    @undead
    def i_am_undead(log):
        log.warning("I'm warning you!")
        log.info("Soap, 2 for $1.99")

Since we didn't specify a ``undead.log_handler`` the logfile will be created by default in ``~/.i_am_undead``

Installation
------------
::

    pip install undead

License
-------

MIT
