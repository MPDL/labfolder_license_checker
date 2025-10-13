# LABFOLDER LICENSE CHECKER

## SET UP

### .env file

```
# DJANGO
SECRET_KEY = super-secret-key
DEBUG = True | False
ALLOWED_HOSTS = 'host-one, host-two' # comma separated string of allowed hosts
DJANGO_LOG_LEVEL = DEBUG | INFO | WARNING | ERROR | CRITICAL # https://docs.djangoproject.com/en/5.2/topics/logging/#loggers 

# DB
POSTGRES_DB = my-db-name
POSTGRES_PASSWORD = db-pswd
POSTGRES_USER = db-user
POSTGRES_HOST = db-host
```

### django database migrations (if needed)

```shell
python manage.py migrate
```

### django super user 

```shell
python manage.py createsuperuser
```

## START DEVELOPMENT SERVER

```shell
python manage.py runserver 0.0.0.0:8000
```