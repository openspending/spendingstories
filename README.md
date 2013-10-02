# Spending Stories

2013, Journalism++  
GNU General Public License

## How to install Spending Stories

### Important notes

This installation guide was created for and tested on __Debian/Ubuntu__ operating systems. 

If you find a bug/error in this guide please submit a pull request.

### Overview

The Spending Stories installation consists of setting up the following components: 


1. Set up your python environnement
1. Install dependencies
1. Set up the database (example with MySQL)
1. Run server (example with mod_wsgi from apache)

### 1. Set up your python environnement

**a. Install python packages:**

```bash
sudo apt-get install build-essential git-core python python-pip python-dev
```

**b. Install virtualenv** a tool to isolate your dependencies

```bash
sudo pip install virtualenv
```

**c.  Download the project**
```bash
git clone https://github.com/jplusplus/okf-spending-stories.git
```

**d.  Create the virtualenv folder for this project**
  > Every python dependencies will be installed in this folder to keep your system's environnement clean.

```bash
cd okf-spending-stories
virtualenv venv --no-site-packages --distribute --prompt=SpendingStories
```

**e. Activate your new virtualenv**

```bash
source .env
```
  > Tips: you can install [autoenv](https://github.com/kennethreitz/autoenv) to source this file automatically each time you `cd` this folder.

### 2. Install dependencies
**a. Install python modules required**

```bash
pip install -r requirements_core.txt
```

**b. Install compilers for *Less* and *CoffeeScript* **

__If you don't have already nodejs installed__:

```bash
sudo apt-get update
sudo apt-get install python-software-properties g++ make
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs
```

and then install them

```bash
cat npm_requirements.txt | sudo xargs npm -g install
```

### 3. Set up the database

**a. Configure the file `webapp/settings.py`**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME'    : 'dev.db', # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER'    : '',
        'PASSWORD': '',
        'HOST'    : '', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT'    : '', # Set to empty string for default.
    }
}
```

Currently, the dataset backend is sqlite3, very easy to use for development.
You can change it by _mysql_, _postgres_ or _oracle_.

#### Example with MySQL

For MySQL, you will need to install mysql-python, like that:

    sudo apt-get install libmysqlclient-dev
    pip install mysql-python

and create the database

    mysql -u root -p
    mysql>  CREATE DATABASE IF NOT EXISTS `<database_name>` DEFAULT CHARACTER SET `utf8` COLLATE `utf8_unicode_ci`;
    mysql> \q


**b. Syncing the database  **

To create the tables in the database and put some data like categories and currencies, please run and provide asked informations

```bash
python manage.py syncdb && python manage.py migrate
```

### 4. Run server

**a. For development**

```bash
python manage.py runserver
```

**b. For production**

You have a lot a choice to deploy this application.  
Take a look on this documentation : [Django - deployment](https://docs.djangoproject.com/en/1.5/howto/deployment/)

Keep in mind that assets are already served by the wsgi server with [dj-static](https://github.com/kennethreitz/dj-static) if you're using our [wsgi.py file](https://github.com/jplusplus/okf-spending-stories/blob/master/webapp/wsgi.py)

Dependency:

    sudo apt-get install libapache2-mod-wsgi

Please see the [documentation](https://docs.djangoproject.com/en/1.5/howto/deployment/wsgi/modwsgi/)

```apacheconf
WSGIScriptAlias / /<PATH_TO_PROJECT>/webapp/wsgi.py
WSGIPythonPath /<PATH_TO_PROJECT>:/<PATH_TO_PROJECT>/venv/lib/python2.6/site-packages:/<PATH_TO_PROJECT>/libs

<Directory /<PATH_TO_PROJECT>/webapp>
<Files wsgi.py>
Order deny,allow
Allow from all
</Files>
</Directory>
```