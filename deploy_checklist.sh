1) Install Gunicorn (or uWSGI)
python -m pip install gunicorn==21.2.0
2) Create *requirements.txt*
python -m pip freeze > requirements.txt
3) Update *ALLOWED_HOSTS* in django_project/settings.py (Prevent HTTP Host header attacks)
ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1"]
4) Create a *Procfile* (Heroku instructions) and *runtime.txt* file (Heroku python ver.)
Procfile
web: gunicorn django_project.wsgi --log-file -

runtime.txt
python-3.10.2
5) Deploy to Heroku
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
