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

  Default: The ``__name__`` attribute of your decorated callable

undead.pidfile
  Path to pidfile.  

  Default: ``~/.{undead.name}/{undead.name}.pid``

undead.log_level
  Log level.  

  Default: ``"WARNING"``

undead.process_name
  The name of the process (that shows up in ps etc.)

  Default: None (No manipulation of process name).

Example
*******

.. code:: python

    import undead

    undead.name = "my-first-daemon"
    undead.process_name = "leDeamon"

    @undead
    def my_daemon_process():
        """ This function will be daemonized. """
        # ...

Logging within the decorated handler
------------------------------------

Just add ``log`` to your decorateds positional arguments and a logger will be passed down. Log away captain!

.. code:: python

    import undead

    @undead
    def i_am_undead(log):
        log.warning("I'm warning you!")
        log.info("Soap, 2 for $1.99")

The logfile will be created in ``~/.i_am_undead``

License
-------

MIT
