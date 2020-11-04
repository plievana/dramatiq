# About
This is just a flask + dramatiq example project

## Run Redis
```bash
> cd Downloads/redis-5.0.5/src
> ./redis-server
```

## Run Flask app
```bash
> export FLASK_ENV=development && env FLASK_APP=app.py venv/bin/flask run
```

## Run dramatiq
```bash
> venv/bin/dramatiq wsgi:broker --watch .
``` 