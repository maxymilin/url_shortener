import logging

from locust import HttpUser, task, between

from random import choice


URLS = [
    "https://www.programcreek.com/python/?CodeExample=list+urls",
    "https://www.peterspython.com/en/?theme=lumen",
    "https://docs.locust.io/en/stable/quickstart.html",
    "https://shekhargulati.com/2018/12/06/locust-load-testing-your-rest-api/",
    "https://docs.djangoproject.com/en/4.0/topics/db/queries/",
    "https://translate.google.com/?hl=uk",
    "https://mail.google.com/",
    "https://www.youtube.com/",
    "https://peps.python.org/pep-0492/",
    "https://peps.python.org",
    "https://www.rada.gov.ua/",
]


class AppUser(HttpUser):
    wait_time = between(1, 4)

    shortener_page = "http://127.0.0.1:8000/shorten_url"
    key = "count"
    url = None

    # @task
    # def index_page(self):
    #     self.client.get("/")

    # @task
    # def count(self):
    #     self.client.get("/count")

    # @task
    # def get_top(self):
    #     self.client.get("/top10")

    @task(1)
    def shortener_url(self):
        url = choice(URLS)
        body = {"target_url": url}
        with self.client.post(
            self.shortener_page,
            json=body,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                error_msg = "Shortener url: response.status_code = {}, expected 200, url = {}".format(
                    response.status_code, choice(URLS)
                )
                logging.error(error_msg)
                response.failure(error_msg)

            response_dict = response.json()
            if "key" not in response_dict:
                error_msg = "Shortener url: data not in response_dict, url = {}".format(
                    url
                )
                logging.error(error_msg)
                response.failure(error_msg)

            url = response_dict["target_url"]
            self.key = response_dict["key"]
            logging.debug(
                "Shortener url create: for url = {}, key = {}".format(url, self.key)
            )

    # @task
    # def get_top(self):
    #     with self.client.get(f"/{self.key}", catch_response=True) as response_out:
    #         if response_out.status_code == 200:
    #             logging.debug(f"Reaching full url: reach full URL: {self.url}")
    #         else:
    #             error_msg = 'Cant reach full url by short representation: key = {}'.format(self.key)
    #             logging.error(error_msg)
    #             response_out.failure(error_msg)
