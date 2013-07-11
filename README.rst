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

Installation
------------
::

    pip install undead

Settings
--------

undead.name
  Name of the logger and process.

  Default: ``__name__`` of decorated callable

undead.pidfile
  Path to pidfile.  

  Default: ``~/.{undead.name}/{undead.name}.pid``

undead.working_directory
  Path to working directory.  

  Default: ``"/"``

undead.log_level
  Log level.  

  Default: ``"WARNING"``

undead.process_name
  The name of the process (that shows up in ps etc.)

  Default: None (No manipulation of process name)

Example
*******

.. code:: python

    import undead
    from logbook import SyslogHandler

    undead.name = "Tangina Barrons"
    undead.pid = "/var/log/tangina.pid"
    undead.working_directory = "/var/www"
    undead.log_level = "ERROR"

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

The logfile will be created by default in ``~/.i_am_undead``

License
-------

MIT
