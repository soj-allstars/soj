# soj - STU(Shit) Open Judge

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

## Production
Configure files to refer to:
### Daphne (supervisor)
conf.d/soj-backend.conf
```
[fcgi-program:soj]
# TCP socket used by Nginx backend upstream
socket=tcp://localhost:8000

# Directory where your site's project files are located
directory=/root/soj

# Each process needs to have a separate socket file, so we use process_num
# Make sure to update "mysite.asgi" to match your project name
command=mkdir -p /run/daphne && /root/soj/venv/bin/daphne -u /run/daphne/daphne%(process_num)d.sock --fd 0 --access-log - --proxy-headers soj.asgi:application

# Number of processes to startup, roughly the number of CPUs you have
numprocs=1

# Give each process a unique name so they can be told apart
process_name=asgi%(process_num)d

# Automatically start and recover processes
autostart=true
autorestart=true

# Choose where you want your log to go
stdout_logfile=/root/soj/soj.log
redirect_stderr=true
```
### Nginx
conf.d/default.conf
```
upstream soj-backend {
    server localhost:8000;
}

server {
    listen       80;
    #server_name  localhost;

    root /var/www;

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        index index.html;
        try_files $uri $uri/ @proxy_to_app;
    }
    location /static/  {
    }

    location @proxy_to_app {
        proxy_pass http://soj-backend;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```
