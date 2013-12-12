# Spending Stories

2013, Journalism++  
GNU General Public License

[![Build Status](https://travis-ci.org/jplusplus/okf-spending-stories.png?branch=master)](https://travis-ci.org/jplusplus/okf-spending-stories)

## Overview

1. [How to install Spending Stories](#how-to-install-spending-stories)
1. [Presentation of the application](#presentation-of-the-application)
1. [How to customize Spending Stories](#how-to-customize-spending-stories)
1. [How to translate Spending Stories](#how-to-translate-spending-stories)
1. [Update stories with last currencies and cpi](#update-stories-with-last-currencies-and-cpi)

## How to install Spending Stories

### Important notes

This installation guide was created for and tested on __Debian/Ubuntu__ operating systems. 

If you find a bug/error in this guide please submit a pull request.

### Overview

The __Spending Stories__ installation consists of setting up the following components: 

1. [Set up your python environment](#1-set-up-your-python-environment)
1. [Install dependencies](#2-install-dependencies)
1. [Set up the database (example with MySQL)](#3-set-up-the-database)
1. [Run server (example with mod_wsgi from apache)](#4-run-server)
2. [Set up your superuser](#5-set-up-your-superuser)

### 1. Set up your python environment

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
  > Every python dependencies will be installed in this folder to keep your system's environment clean.

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

__b. Install compilers for *Less* and *CoffeeScript*__

If you don't have already nodejs installed:

```bash
sudo apt-get update
sudo apt-get install python-software-properties g++ make
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs
```

and then install them

```bash
npm install
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
[Documentation](https://docs.djangoproject.com/en/1.5/ref/databases/)

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

Please see the [documentation](https://docs.djangoproject.com/en/1.5/howto/deployment/wsgi/modwsgi/) about the deployement with mod_wsgi.

This is a apache configuration which loads the virtualenv : 

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

### 5. Set up your superuser

In order to add [stories][wiki-stories] you have to configure your user base. 
If you already synced your database you must have been prompted to configure a
superuser. 

If you skipped this step then you have to run the following command: 

```
python manage.py createsuperuser
```

## Presentation of the application

__Spending Stories__ is built with [Django](https://www.djangoproject.com/), a Python Web framework.

It's composed of :

* a Web application
* an API (Available end-points listed on the page `http://<domain_name>/api`)
* some scripts to update data (with a new inflation by example)  


HTML pages are located in `webapp/templates`  
Static files (css, javascript, images etc...) are located in `webapp/static`


## How to customize Spending Stories

Spending Stories uses [Twitter Bootstrap](http://getbootstrap.com/) for its style.

### Title

Spending Stories' title is defined in a [translation variable](#add-or-edit-translation): `HEADER_APP_TITLE`. However, if you want to change the HTML title tag, you have to manually modify it in `webapp/templates/base.html`.

### Colors

Colors are defined in [less](http://lesscss.org/) variables. They can be overridden in `webapp/static/less/base.less`.

Notable variables:

* `body-bg`: defines the page background
* `brand-primary`: defines color for links, buttons and sticky cards' background
* `strat-main-color`: defines the visualization background color
* `text-color`: defines the color for most of the texts

Acceptable values are hexadecimal colors, rgb colors or [HTML color names](https://en.wikipedia.org/wiki/Web_colors#HTML_color_names):

```css
@body-bg: rgb(80, 80, 80);
@strat-main-color: #403F3F;
@text-color: black;
```

## How to translate Spending Stories

The Spending Stories translation is focused on the front-end of the application.
However we're also using the django default translation system to translate some
string that come from the django application (the server) of this project.

The front-end translation system is composed of the following tools:

- [angular-translate](http://pascalprecht.github.io/angular-translate/), make angular application translation easy.  
- [jplusplus/grunt-angular-translate](https://github.com/jplusplus/grunt-angular-translate) , a fork of [grunt-angular-translate](https://github.com/firehist/grunt-angular-translate). Automate the update of locales. 

This part covers the following topics: 

- how to add/edit some translation
- add a supported language
- what is not fully translated for the moment
    

### Add or edit translation

#### 1. Add translation in the code/in the template files

You have to choose a translation key. We use the following naming convention:
- the key must be in uppercase and underscore (e.g `A_TRANSLATION_KEY`)
- the key describe what it translate and where.
    - the first part of the key is the name of the script or the template containing the key. <br/>
    Ex: a key in `contribute.html` will start by `CONTRIBUTE_`
    - the last part is the description of the content, or the word if it can be described otherwise.<br/>
    Ex: the translation key of the 'Compare' button contained in the `header.html` template will be `HEADER_COMPARE_BUTTON`

> Note: the grunt task for translation key collection is handled by a grunt 
task and therefor is really limited: it may not detect your translation keys 
for many reasons because of its design. To avoid that follow these advises:
>
  1. Prefer filter notation over directive notation in your templates files:
      ``` html
      <!-- good: --> 
      <a href="">[[ 'MY_TRADUCTION' | translate ]]</a>
      <!-- not good: --> 
      <a href="" translate>MY_TRADUCTION</a>
      ```
>  
  2. Avoid dynamic keys in your coffescript files and keep the dollar prefix
      ``` coffee
      # good 
      my_string = $translate('GOOD_KEY_IS_GOOD')
      # bad -> translate service is missing its dollar prefix, it will not detect this key
      my_string = translate('GOOD_KEY')
      # bad -> it's a dynamic key, scripts are not evaluated so it will not detect this key either
      my_key = 'GOOD_KEY_SEEMS_GOOD'
      my_string = $translate(my_key)

#### 2. Launch `python manage.py makemessages` from the `webapp` folder
This will produce the collection of every translation keys contained in html, 
coffee & python files.

#### 3. Update the new generated locales files

This files contains all the translation keys and their translation values, they're located at:
  - `/webapp/static/locales/<locale code>.json` for static application translations
  - `/webapp/locale/<locale code>/LC_MESSAGES/django.po`  for the django application translations

#### 4. Compile the new django messages with `python manage.py compilemessages` from the `webapp` folder

### Add a language

If you want to support a new language in your Spending Stories instance you must change django's settings.
You must update the `webapp/settings.py` file and look for the `LANGUAGES` variable. This is where we store
the list of supported languages, by default we only support english language. 

```python
LANGUAGES = (
  ('en_GB', _('English')),
  # add your new language here
)
```

### What is not fully translated

##### User query

User query comprehension works only in French & English for the moment.
The way we understand the amounts and currencies entered by user is based on a fuzzy search. 
This means all terms that will be recognized have to be entered in an array. 
If you look at the [getSearchSetData](https://github.com/jplusplus/okf-spending-stories/blob/master/webapp/static/coffee/services/Comprehension.coffee#L140)  method in the `Comprehension`
service you can see all translated term in our array. <br/>

This way of doing cannot work with German for instance because a lot of numbers are constructed with
others. 
Fuzzy search can work but the search data set (the data that will be used to perform the search) have to be build
by an algorithm because of the tremendous amount of numbers. 

## Update stories with last currencies and cpi
It's important to note that the conversion rates & the consumer price indexes we use 
to deal with [inflation][wiki-inflation] need to be refreshed by hand: 

```bash
./scripts/update_cpi.py
./scripts/update_currencies.py <api key from https://openexchangerates.org/signup/free>
./scripts/recompute_stories.py
```

and restart the application in order to reload the new dataset.

[wiki-stories]:http://github.com/jplusplus/okf-spending-stories/wiki/About-this-project#stories
[wiki-inflation]:http://github.com/jplusplus/okf-spending-stories/wiki/About-this-project#inflation
