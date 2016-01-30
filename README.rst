===============================
tracker_project_django_channels
===============================

A simple Django project to report and track geo-located incidents within certain areas of interest. Whenever a new incident occurs the user is reported in real-time and the event is marked in a map (using `Google Maps JavaScript API <https://developers.google.com/maps/documentation/javascript/>`_). It's is possible to report the locations manually, but there's also a view that uses the `geolocator <https://github.com/onury/geolocator>`_ library to automatically detect the user's location.

The default configuration uses `PostgreSQL <http://www.postgresql.org/>`_ with the `PostGIS <http://postgis.net/>`_ extensions as database back-end, but it can also work with other GeoDjango compatible databases like `SQLite <http://www.sqlite.org/>`_ + `SpatiaLite <https://www.gaia-gis.it/fossil/libspatialite/index>`_.

Real-time notifications
=======================

This project created to demonstrate how to use `GeoDjango <https://docs.djangoproject.com/en/1.7/ref/contrib/gis/>`_ as well as sending real-time notifications using `django channels <https://github.com/andrewgodwin/channels>`_ with the `Redis<http://redis.io/>`_ backend.

Requirements
============

Before you can run this project, the following packages need to be installed:

Ubuntu
------

* git
* python-dev
* postgresql
* postgresql-server-dev-all
* postgis
* python-virtualenv
* redis-server

Fedora
------

* git
* python-devel
* postgresql-server
* libpqxx-devel
* postgis
* python-virtualenv
* redis-server

Installation
============

Clone the repository: ::

    $ git clone --branch use-django-channels git@github.com:abarto/tracker-project.git

Create and activate the virtual environment: ::

    $ cd tracker-project/
    $ virtualenv venv/
    $ . venv/bin/activate

Install the requirements: ::

    (venv)$ pip install -r requirements.txt

Initialize nodeenv, and install bower: ::

    (venv)$ nodeenv -p
    (venv)$ npm install -g bower

Create the database and the database user, install the PostGIS extensions: ::

    sudo -u postgres psql --command="CREATE USER tracker_project WITH PASSWORD 'tracker_project';"
    sudo -u postgres psql --command="CREATE DATABASE tracker_project WITH OWNER tracker_project;"
    sudo -u postgres psql --command="GRANT ALL PRIVILEGES ON DATABASE tracker_project TO tracker_project;"
    sudo -u postgres psql --command="CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" tracker_project

Initialize the database and set-up the Django environment: ::

    (venv)$ cd tracker_project/
    (venv)$ python ./manage.py migrate
    (venv)$ python ./manage.py bower_install

At this point it is possible to run the development server using the following commands ::

    (venv)$ python ./manage.py runserver

and

    (venv)$ python ./manage.py runwsserver

for the WebSocket server.

Running the application
=======================

As mentioned in the `django channels <https://github.com/andrewgodwin/channels>`_ in order to run the application using websockets we need at least and interface server and a worker are needed. We're going to use uWSGI to serve traditional HTTP requests and act as a worker, and the default WebSocket server that comes with Django channels:

::

    (venv)$ uwsgi --chdir=/path/to/tracker_project/tracker_project \
      --module=tracker_project.wsgi:application \
      --env DJANGO_SETTINGS_MODULE=tracker_project.settings \
      --master --pidfile=/path/to/tracker_project/tracker_project-master.pid \
      --http=127.0.0.1:8000 \
      --processes=5 \
      --harakiri=20 \
      --max-requests=5000 \
      --vacuum \
      --home=/path/to/tracker_project_venv/

and the WebSocket server:

::

    (venv)$ python ./manage.py runwsserver

::

Please notice that the application won't server the static files, so before you can start using it, you need to run the ``collectstatic`` management command: ::

    (venv)$ python ./manage.py collectstatic

and then use a regular HTTP server like `nginx <http://nginx.com>`_ to server the files. We've included sample configuration files for NGINX and Supervisor.

Vagrant
-------

A `Vagrant <https://www.vagrantup.com/>`_ configuration file is included if you want to test the project.

Feedback
========

Comments, issues and pull requests are welcome. Don't hesitate to contact me if you something a could have done better.
