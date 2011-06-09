# How to use these tools

Create and populate the database:

    $ cat rod-schema.sql | sqlite3 rod.db
    $ bzcat rod-complete.sql.bz2 | sqlite3 rod.db

Install [Flask](http://flask.pocoo.org) and run the viewer:

    $ virtualenv --distribute pyenv
    $ source pyenv/bin/activate
    $ pip install flask
    $ python viewer.py