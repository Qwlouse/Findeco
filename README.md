Findeco
=======

Working Repository for the new BasDeM / DisQussion joint venture.


Requirements
------------
* Python 3.4
* Django 1.8
* Django-Cron 0.4

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

    
