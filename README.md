barkingowl-frontend
===================

A very lite frontend for the barkingowl document scraping system.

Getting started is easy!

First, to use barkingowl you need to install RabbitMQ.  You can find information about installing RabbitMQ on your
system here: [http://www.rabbitmq.com/download.html](http://www.rabbitmq.com/download.html)

Next, execute these commands to launch the server:

    $ virtualenv barkingowl-frontend-venv
    $ source barkingowl-frontend-venv/bin/activate
    $ git clone https://github.com/thequbit/barkingowl-frontend
    $ pip install barkingowl
    $ cd barkingowl-frontend
    $ python server.py

This will launch a flask-based web server on port 8067.  You can access the site by going to this url:

    http://127.0.0.1:8067/

You will see a single, simple page.  On this page there are two main functions: 1) upload a csv file to the site so it can be configured into the barkingowl dispatcher, and 2) shutdown the entire barkingowl system.

For more information head over to the [wiki](https://github.com/thequbit/barkingowl-frontend/wiki)
