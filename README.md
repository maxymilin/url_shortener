# url_shortener

A URL shortener API using python.

## The requirements

The web-service should have a POST /shorten_url endpoint that receives a JSON body with the URL to shorten.
A successful request will return a JSON body with the shortened URL.
If web-service gets a request with the shortened URL then the user should be redirected to the original URL or returned the contents of the original URL.
URL must go through appropriate validation before shorting, and return appropriate error responses if the URL is not valid.


## Start

To build the appropriate Docker container, run the following from your terminal:

```cmd
docker-compose up -d --build
```

To run container:

```cmd
docker-compose up -d --build
```

Aplication run  http://0.0.0.0:8000/