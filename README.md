# How to use these tools

Create and populate the database:

    $ cat rod-schema.sql | sqlite3 rod.db
    $ bzcat rod-complete.sql.bz2 | sqlite3 rod.db

Install [Flask](http://flask.pocoo.org) and run the viewer:

    $ virtualenv --distribute pyenv
    $ source pyenv/bin/activate
    $ pip install flask
    $ python viewer.py

# Initial extraction

The data has been extracted from an MS Access (JET) database, with the help of [mdbtools](http://mdbtools.sourceforge.net/).

First extract a basic schema. This is a rudimentary conversion, and the end result required extensive editing to make the output SQLite-compatible. PRIMARY KEY and FOREIGN KEY constraints were also added where obvious.

    $ mdb-schema rod.mdb > rod-schema.sql

Now get a list of tables we're interested in:

    $ ROD_TABLES="$(mdb-tables rod-snap-20100426.mdb | tr ' ' '\n' | grep ROD)"

Extract each of these tables to CSV:

    $ echo $ROD_TABLES | while read table; do mdb-export rod-snap-20100426.mdb $table > $table.csv; done

You can optionally convert these CSVs to SQL "INSERT" statement files using `csv2sql.py`:

    $ echo $ROD_TABLES | while read table; do python csv2sql.py $table < $table.csv | bzip2 > $table.sql.bz2; done

Note that you will need to ensure you load the tables into the SQL database in the correct order to ensure FOREIGN KEY constraints are met. In particular, load ROD_GRANTS first, and ROD_OUTPUTS second.
