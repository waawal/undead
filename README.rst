undead
===========

.. image:: http://dribbble.s3.amazonaws.com/users/158965/screenshots/826605/mr_z.gif
   :alt: This house is clean.

Dead Easy ``*NIX`` Daemons, in ``Python``!

.. code:: python

    import undead

    @undead
    def my_daemon_process():
        """ This function will be daemonized. """
        from time import sleep
        while True:
            sleep(10)

Settings
--------

undead.name
  Name of the logger.

  Default: ``__name__`` of decorated callable

undead.pid
  Path to logfile.  

  Default: ``~/.undead.name/undead.name.pid``

undead.log_level
  Log level.  

  Default: ``"WARNING"``

undead.log_handler
  The logbook handler.

  Default: ``~/.undead.name/undead.name.log``

Example
*******

.. code:: python

    import undead
    from logbook import SyslogHandler

    undead.name = "Tangina Barrons"
    undead.pid = "/var/log/tangina.pid"
    undead.log_level = "ERROR"
    undead.log_handler = SyslogHandler("My Daemon", level="ERROR")

    @undead
    def my_daemon_process():
        """ This function will be daemonized. """
        # ...

Logging in the decorated handler
--------------------------------

Just add ``log`` to your decorateds signature, and the logger will be passed down. Log away captain!

.. code:: python

    import undead

    @undead
    def some_things_have_to_be_believed_to_be_seen(log):
        log.warning("I'm logging")
        log.info("on multiple levels!")

As we haven't specified a ``undead.log_handler`` the logfile will be created in ``~/.some_things_have_to_be_believed_to_be_seen``

Installation
------------
::

    pip install undead

Dependencies
------------

``logbook``

License
-------

MIT