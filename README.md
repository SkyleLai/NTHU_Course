[![Build Status](https://travis-ci.org/henryyang42/NTHU_Course.svg?branch=master)](https://travis-ci.org/henryyang42/NTHU_Course)
# NTHU Course

A system that fetch the course data and provide service that is instinctive, easy to use.


# Getting Started


## Install dependency

- python
    - version: >= 3.5

- tesseract
    - version: >= 3.03
    - mac: `brew install tesseract`
    - ubuntu: `sudo apt-get install tesseract-ocr`
    - arch linux: `sudo pacman -S tesseract tesseract-data-eng`

- mariadb
    - version: >= 10.0.27
    - mac: `brew install mariadb`
    - ubuntu: `sudo apt-get install mariadb-server`
    - arch linux: `sudo pacman -S mariadb`


## Install and Setup Virtualenv (optional)

We highly recommend developers to setup environment with **virtualenv**.

You can install this package by typing `pip3 install virtualenv` in your console.


## Basic Settings for Database

Create database for models.

```bash
mysql -u root -p
CREATE DATABASE `<database name>`;
CREATE USER '<mysql username>'@'localhost' IDENTIFIED BY '<mysql password>';
GRANT ALL PRIVILEGES ON <database name>.* TO '<mysql username>'@'localhost';
```

By default, the system will find a configuration file in `NTHU_Course/mysql.ini`.

So you need to create it and put your settings in this file. The following
 script is the example for `mysql.ini`.

```ini
[client]
database = <database name>
user = <mysql username>
password = <mysql password>
host = <mysql server ip> ; localhost for local server
port = <mysql server port> ; which default is 3306
default-character-set = utf8
```


## Build the System.

Typing the commands below may help you build this system.

```bash
virtualenv VENV --python=python3
source VENV/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py crawl_course
python3 manage.py update_index
```

To update all syllabus, use ``python3 manage.py update_syllabus``
To clear all contents in db, use ``python3 manage.py crawl_course --clear``
To wipes out your entire search index, use `python3 manage.py clear_index`

## Launch

```bash
python3 manage.py collectstatic
python3 manage.py runserver --insecure
```



# Heroku settings
To use it in heroku, you have to set the following environment variables

```bash
TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/tessdata
BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git
DJANGO_SETTINGS_MODULE=NTHU_Course.settings.heroku
SECRET_KEY=hard-to-guess-string
```

this can be achieved by ``heroku config:set`` or the web panel
