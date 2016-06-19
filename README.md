# Chronos API
    The Kick-Ass Time keeper.

## Manual Setup
The app is configured to run in development mode.

Base path for application is `/path/to/repo/core`

* setup the python environment using `pip install -r requirements.txt`
* create mysql database `create database chronos;`
* copy `core/settings.py.sample` to `core/settings.py`
* update settings.py with mysql password #L12
* with `cd /path/to/repo/core` run `python manage.py db upgrade`
* with `cd /path/to/repo/core` run `python -m scripts.mySqlDefaults`
* Add `/path/to/repo/chronos_nginx.conf` in `nginx/site-enabled`. Make necessary updates in the template.
* Add `/path/to/repe/uwsgi_chronos.conf` in `/init/uwsgi-chronos.conf`. Make necessary updates in the template.
