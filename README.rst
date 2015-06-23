Findeco
=======

Working Repository for the new BasDeM / DisQussion joint venture.

|unix_build| |coverage|

Requirements
------------
* Python 3.4
* Django 1.8
* Django-Cron 0.4

Set Up
------
After cloning the repo run from the Findeco directory:

    python manage.py migrate
    python manage.py initial_data

And after each git pull run the following commands to migrate the database:

    python manage.py migrate


License
-------
This project is dually licensed under the terms of the 
`GPL3 <http://opensource.org/licenses/GPL-3.0>`_ and the 
`MPL2 <https://www.mozilla.org/MPL/2.0/>`_.

.. |unix_build| image:: https://img.shields.io/travis/qwlouse/findeco.svg?branch=master&style=flat
    :target: https://travis-ci.org/qwlouse/findeco
    :alt: Travis-CI Status

.. |coverage| image:: https://coveralls.io/repos/qwlouse/findeco/badge.svg?branch=master&style=flat
    :target: https://coveralls.io/r/qwlouse/findeco
    :alt: Coverage Report
