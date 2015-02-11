# Game Database Website
## Setup
**Requirements**

* Python 2.7.x
* PostgreSQL 9.3+


### Clone the Repository

        git clone git@github.com:joshsamara/game-website.git

### Set up Postgres

1. Download PostgreSQL 9.3 (or above) and get it running if you haven't already.
   You have 3 options:
    - [http://postgresapp.com/](Postgres.app). Recommended because it's easy on
      OSX.
    - Install via Homebrew (`brew install postgresql`)
    - Download and run the executable from
      [http://postgresql.org/download](postgresql.org)

2. Make a Postgres database and user

        $ psql
        # CREATE USER gameadmin SUPERUSER WITH PASSWORD 'password';
        # CREATE DATABASE gamesite;
        # GRANT ALL PRIVILEGES ON DATABASE "gamesite" to gameadmin;
        # ALTER ROLE gameadmin CREATEDB;
        # ALTER ROLE gameadmin LOGIN;

### Create a [Virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
First install **virtualenv** with pip

        $ pip install virtualenv

It's recommended to also install **virualenvwrapper**

        $ pip install virtualenvwrapper
        $ export WORKON_HOME=~/Envs
        $ source /usr/local/bin/virtualenvwrapper.sh

Then create your **virtualenv**

        $ cd this_project_folder
        $ mkvirtualenv game-site

Now activate your **virutalenv**

If you installed **virtualenvwrapper**:

        $ workon game-site

If you didn't:

        $ source game-site/bin/activate

To deactivate the **virtualenv** use

        $ deactivate

### Install python requirements
With your **virtualenv** activated, run

    $ pip install -r requirements.txt

### Setup Your database
Run the following command to setup your database

    $ ./manage.py migrate

### Make a superuser account
Run the following command, you'll be prompted for to answer questions

    $ python manage.py createsuperuser


### Run the server

    $ ./manage.py runserver_plus

Now visit `localhost:8000` in a web browser to see the website
