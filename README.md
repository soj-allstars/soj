# soj - STU(Shit) Open Judge

## Setup
soj need Python 3.8 to run.

run following commands to setup.
```bash
python -m venv venv
source venv/bin/activate
```
necessary to run 
```bash
apt install python3.8-dev libmysqlclient-dev
pip install -r requirements.txt
```
if encounter twisted installation issue, try one of the following commands, and pip install again
```bash
pip install twisted[tls]
pip install git+git://github.com/twisted/twisted.git
```
finally
```bash
python manage.py migrate
```
### Development
Twisted is not supported on 3.8 on Windows, so if develop on Windows, find the solution below

[Solution](https://stackoverflow.com/questions/58908293/i-keep-getting-notimplementederror-error-when-starting-django-server)
### Set up for production
#### MySQL
#### Daphne
#### Nginx