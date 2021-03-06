REST API
********

In this section will describe the REST API.

Authorization Process
=====================

This project use the oAuth 2.0 process ( Draft 31 ).
The Authentications Flow processes supported are two.

    * Application Flow
    * Client-Side Flow


Application Flow
----------------

This is used if the tester is with a web server application ( php, java, python, ruby, C#, etc.).
The sequence is described in this image.


.. figure:: images/appflow.png
    :align: center


The scenario is redirecting the User-Agent to the login page ( popup etc.).
The url to call from the Client Application is. ::


    GET http://localhost:8888/oauth/auth

is **Mandatory** add the following parameter to this url

    * *client_id*: * This is the client id added to the database in the client table *
    + *response_type*: * For the Application Flow this value is ``code`` *
    * *redirect_uri*: * This is the redirect uri added into the database in the client table for the client_id *
    * *scope*: * The scope in this project is **not processed**, have only one scope and is call *

.. warning::

    This project have a test page for the redirect process, this page is ::

    http://localhost:8888/test

    this page return the code and the token after the grant process and the token creation!


So, in conclusion the final url for the client auth is. ::

    GET http://localhost:8888/oauth/auth?client_id=<client_id>&response_type=code&redirect_uri=http://localhost:8888/test&scope=call

After calling this url, the system automatically redirect to the Login-Page, the redirection is a 302 Status Code
The login Page URL where the User-Agent is redirect is: ::

    GET http://localhost:8888/auth/login?client_id=<client_id>&response_type=code&redirect_uri=http://localhost:8888/test&scope=call

The page show JSON formatted String with the parameters attached to the URL.
If the User-Agent is already Logged, the System redirect with a 303 status code to the Grant page.
If the user is not logged in, is necessary to send a post to the same url, with the ``username`` and ``password`` parameters. ::

    POST http://localhost:8888/auth/login

    body_parms:
    client_id=<client_id>&response_type=code&redirect_uri=http://localhost:8888/test&scope=call&username=<user_username>&password=<user_password>


If the login is processed correctly, the System redirect to the Grant Page. This is the process that authorize the Application-ID take some information
of the User-Agent. In a classic project this page show a form with two button, *Accept* *Refuse*. In this project is returned a json string with the parameters
passed to the URL from the login page.
If the User-Agent never have Grnated the Application-ID must be send a POST to the same url: ::

    POST http://localhost:8888/auth/grant

    body_params:
    client_id=<client_id>&response_type=code&redirect_uri=http://localhost:8888/test&scope=call&grant=true

In this example the User-Agent has sent ``grant=true`` so he have accepted the Application Access.
Now the system redirect to the ``redirect_uri`` passed as a parameter.
*if you is used the test page ``http://localhost:8888/test`` you will take the code from the body that show a JSON String.*
The redirect is: ::

    GET http://localhost:8888/test?code=<code>


After this process will be can take the token with the code returned.
To obtain the token you need to send a GET to this url and with thsi parameters. ::


    GET http://localhost:8888/oauth/token?client_id=<client_id>&client_secret=<secret_id>&code=<code>&redirect_uri=http://localhost:8888/test&grant_type=authorization_code


In this URl have one new parameter ``client_secret``. This parameter is one column in the Client Table and is the *password* for the Application.
After call this URL, the System will be redirect to the ``redirect_uri`` , like the code step, this page show in the body a JSON string with the token code, the redirection is with a 303 status code.
The url called is: ::

    GET http://localhost:8888/test#access_token=<token>&token_type=Bearer&expires_in=3600


Now with the token is possible to call the REST Server.

Client-Side Flow
----------------

This Flow is practically the same as the Application-Flow. This is used by Javascript Application ( client-side ).
In the image have the flow view of the process.

.. figure:: images/flowtwo.png
    :align: center

This process will not request the token from a code authentication.
the url flow is: ::


    GET http://localhost:8888/oauth/auth?client_id=<client_id>&response_type=token&redirect_uri=http://localhost:8888/test&scope=call

login redirection: ::



    GET http://localhost:8888/auth/login?client_id=<client_id>&response_type=token&redirect_uri=http://localhost:8888/test&scope=call

Send the post to login the user: ::


    POST http://localhost:8888/auth/login

    body_parms:
    client_id=<client_id>&response_type=token&redirect_uri=http://localhost:8888/test&scope=call&username=<user_username>&password=<user_password>

grant if is not granted, if the customer is granted will be automatically redirect to the redirect_uri: ::

    POST http://localhost:8888/auth/grant

    body_params:
    client_id=<client_id>&response_type=token&redirect_uri=http://localhost:8888/test&scope=call&grant=true

after this step, the system redirect to the page and send the parameters as: ::

    GET http://localhost:8888/test#access_token=<token>&token_type=Bearer&expires_in=3600

Now is possible to call the REST Sever


REST Call Interface
=====================


HowTo send the token for authentication
---------------------------------------

Is possible to send the token in two methods.
as a URL parameter: ::


    GET http://localhost:8888/rest/call?access_token=<access_token>

or in the header: ::


    POST /rest/call HTTP/1.1
    Host: localhost:8888
    User-Agent: PersonalUser-Agent
    Authentication: Bearer <your-token>


Is important to add the ``Bearer`` parameter to stay compliant with the oAuth2 protocol.


Make a call
-----------

Send a POST to this url: ::

    POST http://localhost:8888/rest/call

The parameter to send in the post is ``number=<number_to_call``
If all work well you will obtain a status code 201, in the ``Location`` header you will obtain the GET URL with the token call to get the call information: ::

    RESPONSE:
    HTTP/1.1 201 OK
    Server: xLightweb/2.6
    Content-Length: 0
    Location: http://localhost:8888/rest/call?token_call=<token_call>
    Content-Type: application/x-www-form-urlencoded


Stop a Call
-----------

Send a PUT to this url: ::


    PUT http://localhost:8888/rest/call

And in the PUT body this parameter: ::


    token_call=<token_call>

This method return a status code 200

Get Call info
-------------

To get informations about a call you need to send a GET request: ::

    GET http://localhost:8888/rest/call?token_call=<token_call>

Yu will obtain a JSON string or a xml string with the call information. if have some problems will return 409 error Conflict

Get All Ongoing Calls
---------------------

To get all ongoing calls you need to send a GET to this url whitout any parameter: ::

    GET http://localhost:8888/rest/call

The result is a JSON or a XML string with all the ongoing calls for the logged user.





