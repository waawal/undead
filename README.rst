poltergeist
===========

Dead Easy UNIX Daemons!

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

  Default: `__name__` of decorated callable

poltergeist.pid
  Path to logfile.  

  Default: /tmp/`poltergeist.name`.pid

poltergeist.log_level
  Log level.  

  Default: "WARNING"

poltergeist.file_descriptors
  List of filedescriptors to hold open.

  Default: `[]`


.. code:: python

    import poltergeist

    poltergeist.name = "Tangina Barrons"
    poltergeist.pid = "~/tangina.pid"

    @poltergeist
    def my_daemon_process():
        """ This function will be daemonized. """
        # ...