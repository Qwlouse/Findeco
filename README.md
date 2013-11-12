Findeco
=======

Working Repository for the new BasDeM / DisQussion joint venture.


Requirements
------------
* Python 2.7
* Django 1.4.3
* Django South 0.7.6
* Django Nose 1.3.0

Set Up
---------------
After cloning the repo run from the Findeco directory:

    python manage.py syncdb
    python manage.py migrate findeco
    python manage.py migrate node_storage
    python manage.py migrate microblogging
    python manage.py initial_data

And after each git pull run the following commands to migrate the database:

    python manage.py migrate findeco
    python manage.py migrate node_storage
    python manage.py migrate microblogging

    
