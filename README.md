# soj - STU(Shit) Open Judge

## How to Setup
soj need python3.8 to run.

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
