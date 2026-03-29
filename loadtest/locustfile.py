from locust import HttpUser, task, between
from bs4 import BeautifulSoup
import os
import re
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_PATH = os.path.join(BASE_DIR, "sample.jpg")

class AlbumUser(HttpUser):
    wait_time = between(0.1, 0.5)

    HOME_PATH = "/"
    LOGIN_PATH = "/auth/login/"
    LOGOUT_PATH = "/auth/logout/"
    REGISTER_PATH = "/auth/register/"
    UPLOAD_PATH = "/upload/"

    USERNAME = os.getenv("LOCUST_USERNAME", "loadtest1")
    PASSWORD = os.getenv("LOCUST_PASSWORD", "LoadTest123!")

    def on_start(self):
        self.photo_ids = []
        self.login()
        self.refresh_photo_ids()


    def get_csrf_token(self, path: str, request_name: str = None):
        response = self.client.get(
            path,
            name=request_name if request_name else f"GET {path}"
        )
        soup = BeautifulSoup(response.text, "html.parser")
        token_input = soup.find("input", {"name": "csrfmiddlewaretoken"})
        if token_input and token_input.get("value"):
            return token_input["value"]
        return None

    def login(self):
        token = self.get_csrf_token(self.LOGIN_PATH)
        if not token:
            return

        self.client.post(
            self.LOGIN_PATH,
            data={
                "username": self.USERNAME,
                "password": self.PASSWORD,
                "csrfmiddlewaretoken": token,
            },
            headers={"Referer": f"{self.host}{self.LOGIN_PATH}"},
            name="POST /auth/login/",
            allow_redirects=True,
        )

    @task(1)
    def register_user(self):
        token = self.get_csrf_token(self.REGISTER_PATH)
        if not token:
            return

        username = f"user_{random.randint(1, 1000000)}"

        self.client.post(
            self.REGISTER_PATH,
            data={
                "username": username,
                "password1": "Test123456!",
                "password2": "Test123456!",
                "csrfmiddlewaretoken": token,
            },
            headers={"Referer": f"{self.host}{self.REGISTER_PATH}"},
            name="POST /auth/register/",
            allow_redirects=True,
        )

    def refresh_photo_ids(self):
        response = self.client.get(self.HOME_PATH, name="GET /")
        ids = set()

        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]

            m1 = re.fullmatch(r"/(\d+)/", href)
            if m1:
                ids.add(int(m1.group(1)))

            m2 = re.fullmatch(r"/(\d+)/delete/", href)
            if m2:
                ids.add(int(m2.group(1)))

        self.photo_ids = sorted(ids)

    def ensure_has_photo(self):
        if not self.photo_ids:
            self.upload_photo()
            self.refresh_photo_ids()

    @task(4)
    def photo_list(self):
        self.client.get(self.HOME_PATH, name="GET /")

    @task(2)
    def photo_list_sorted_by_name(self):
        self.client.get("/?sort=name", name="GET /?sort=name")

    @task(2)
    def photo_list_sorted_by_date(self):
        self.client.get("/?sort=date", name="GET /?sort=date")

    @task(3)
    def photo_detail(self):
        self.ensure_has_photo()
        if not self.photo_ids:
            return

        photo_id = random.choice(self.photo_ids)
        self.client.get(f"/{photo_id}/", name="GET /<id>/")

    @task(2)
    def upload_photo(self):
        token = self.get_csrf_token(self.UPLOAD_PATH, "GET /upload/")
        if not token:
            return

        if not os.path.exists(SAMPLE_PATH):
            return

        with open(SAMPLE_PATH, "rb") as image_file:
            self.client.post(
                self.UPLOAD_PATH,
                data={
                    "name": f"loadtest-{random.randint(1, 100000)}",
                    "csrfmiddlewaretoken": token,
                },
                files={
                    "image": ("sample.jpg", image_file, "image/jpeg")
                },
                headers={"Referer": f"{self.host}{self.UPLOAD_PATH}"},
                name="POST /upload/",
                allow_redirects=True,
            )

        self.refresh_photo_ids()

    @task(1)
    def delete_photo(self):
        self.refresh_photo_ids()

        if not self.photo_ids:
            return

        photo_id = random.choice(self.photo_ids)
        delete_path = f"/{photo_id}/delete/"

        token = self.get_csrf_token(delete_path, "GET /<id>/delete/")
        if not token:
            return

        self.client.post(
            delete_path,
            data={"csrfmiddlewaretoken": token},
            headers={"Referer": f"{self.host}{delete_path}"},
            name="POST /<id>/delete/",
            allow_redirects=True,
        )

        self.refresh_photo_ids()

    @task(1)
    def relogin(self):
        self.client.get(self.LOGOUT_PATH, name="GET /auth/logout/")
        self.login()
        self.refresh_photo_ids()