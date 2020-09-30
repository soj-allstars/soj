# soj - STU(Shit) Online Judge

## Setup
### MySQL
Install MySQL first, recommend to use MySQL 8.0.

Create database and user, and grant privileges:
```
> create database soj;
> create user 'soj'@'localhost' identified by 'soj';
> grant all on soj.* to 'soj'@'localhost';
```

### soj
soj need Python 3.8 to run. Clone this repo first, and cd to the directory that cloned to.

Activate a [virtual environment](https://docs.python.org/3/library/venv.html):
```bash
$ python -m venv venv
$ source venv/bin/activate
```
Install dependencies:
```bash
$ apt install python3.8-dev libmysqlclient-dev
$ pip install -r requirements.txt
```
If encounter twisted installation issue, try install twisted through git, and pip install again:
```bash
$ pip install git+git://github.com/twisted/twisted.git
```
Migrate database:
```bash
$ python manage.py migrate
```
Finally run dev server:
```
$ python manage.py runserver 0.0.0.0:80
```
### Issues
Twisted is not supported on Python 3.8 on Windows, so if develop on Windows, find the solution below:

[Solution](https://stackoverflow.com/questions/58908293/i-keep-getting-notimplementederror-error-when-starting-django-server)
