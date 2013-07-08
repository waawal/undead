poltergeist
===========

Dead Easy ``*NIX`` Daemons, in ``Python``!

.. image:: http://www.pajiba.com/assets_c/2013/05/tumblr_m7nqnc5zVp1rokxsko1_500-thumb-500x206-69830.gif
   :alt: This house is clean.

.. code:: python

    import poltergeist

    @poltergeist
    def my_daemon_process():
        """ This function will be daemonized. """
        from time import sleep
        while True:
            sleep(10)

Settings
--------

poltergeist.name
  Name of the logger.

  Default: ``__name__`` of decorated callable

poltergeist.pid
  Path to logfile.  

  Default: ``~/.poltergeist.name/poltergeist.name.pid``

poltergeist.log_level
  Log level.  

  Default: ``"WARNING"``

poltergeist.log_handler
  The logbook handler.

  Default: ``~/.poltergeist.name/poltergeist.name.log``

Example
*******

.. code:: python

    import poltergeist
    from logbook import SyslogHandler

    poltergeist.name = "Tangina Barrons"
    poltergeist.pid = "/var/log/tangina.pid"
    poltergeist.log_level = "ERROR"
    poltergeist.log_handler = SyslogHandler("My Daemon", level="ERROR")

    @poltergeist
    def my_daemon_process():
        """ This function will be daemonized. """
        # ...

Logging in the decorated handler
--------------------------------

Just add ``log`` to your decorateds arguments, and the logger will be passed down. Log away captain!

.. code:: python

    import poltergeist

    @poltergeist
    def some_things_have_to_be_believed_to_be_seen(log):
        log.warning("I'm logging")
        log.info("on multiple levels!")

As we haven't specified a ``poltergeist.log_handler`` the logfile will be created in ``~/.some_things_have_to_be_believed_to_be_seen``

Installation
------------
::

    pip install poltergeist

Dependencies
------------

``logbook``

License
-------

MIT