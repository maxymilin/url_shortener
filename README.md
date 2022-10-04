# url_shortener

A URL shortener API using python.

## The requirements

The web-service should have a POST /shorten_url endpoint that receives a JSON body with the URL to shorten.
A successful request will return a JSON body with the shortened URL.
If web-service gets a request with the shortened URL then the user should be redirected to the original URL or returned the contents of the original URL.
URL must go through appropriate validation before shorting, and return appropriate error responses if the URL is not valid.


## Prepare Environment

### Create project structure

Create the app folder:

```bash
$ mkdir shortener_app
```

In app forlder create __init__.py file what shows shortener_app folder is a package:

```bash
$ touch shortener_app/__init__.py
```

### Create a virtual environment

To create virtual environment using venv package:

```bash
$ python3 -m venv .venv
```

Activation virtual environment:

```bash
$ source .venv/bin/activate
```