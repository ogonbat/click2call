
Requirements
------------
    * `Python 2.7 <http://python.org/download/>`_
    * `Tornado 2.3 <http://www.tornadoweb.org/>`_
    * `PostgreSQL <http://www.postgresql.org/>`_


Installation
------------

Is possible to use this project in a virtualenv, install before a virtual env: ::


    $ virtualenv venv --distribute
    New python executable in venv/bin/python
    Installing distribute...............done.
    Installing pip...............done.


To activate the environment. ::


    $ source venv/bin/activate

Now if you are in the root project folder you can use the requirements files to install all the the required packages ::


    $ pip install -r requirements.txt

If all work well you have the project ready to use


Usage
-----

If you have activate your virtualenv you can launch the project form the root folder. ::


    $python manage.py


The default value lauch a web server to the port ``8888`` the Web Server accept internal connections
``http://localhost:8888`

