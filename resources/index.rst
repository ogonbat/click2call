.. Click2Call documentation master file, created by
   sphinx-quickstart on Fri Aug 17 03:25:13 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ClickToCall documentation!
=================================================

CLick2Call is Python project test with tornado and PostgreSQL database Server.

This project was created for a demo and is not a complete click to call service.

The project support:

    * Client App registration ( oAuth 2.0 )
    * User-Agent login
    * create a call, not SIP signaling or RTP flux, is only a REST call that open a call SESSION
    * terminate a call
    * limit ongoing and outgoing call for a user ( if the user is registered with different apps, the limitation work as well )
    * a very basic admin REST interface to check the user call status and the call informations.


.. include:: ./readme.rst

Contents
========

.. toctree::
    :maxdepth: 2

    rest
    code

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

