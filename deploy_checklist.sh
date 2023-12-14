1) Create *requirements.txt*
python -m pip freeze > requirements.txt
2) Update *ALLOWED_HOSTS* in django_project/settings.py (Prevent HTTP Host header attacks)
ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1"]
3) Create a env file, Dockerfile, docker-compose and entrypoint for dev env.
4) Do the same for production


: '
3) Create a *Procfile* (Heroku instructions) and *runtime.txt* file (Heroku python ver.)
Procfile
web: gunicorn proj.wsgi --log-file -

runtime.txt
python-3.10.2
4) Deploy to Heroku
heroku login
# Create new app
heroku create  # Check with git remote -v
# Ignore static files
heroku config:set DISABLE_COLLECTSTATIC=1
# Push
git push heroku main
# Make heroku live
heroku ps:scale web=1
# Open URL
heroku open
# Connect to Heroku (to run migrate)
heroku run bash
# Check logs
heroku logs --tail
5) Install Postgre for Heroku
# proj/settings.py
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}
# requirements.txt
dj-database-url 
psycopg2

TODO
1) Configure static files, install whitenoise,  collectstatic
2) Setup Docker containers
3) *.gitignore*
4) Create a Heroku project, push, start dyno web process
5) *DEBUG* set to *False*
6) *SECRET_KEY*
7) Prod. db.
8) Switch to VM + Apache/nginx

---

https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
'
