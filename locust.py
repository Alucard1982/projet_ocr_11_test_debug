import time

from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("")

    def on_start(self):
        self.client.post("club", data={"email": "john@simplylift.co"})

    @task
    def showSummary(self):
        self.client.get("showSummary/Simply_Lift")

    @task
    def book(self):
        self.client.get("book/Fall_Classic/Simply_Lift")

    @task
    def purchasePlaces(self):
        self.client.post("purchasePlaces", data={"club": "Simply_Lift", "competition": "Fall_Classic", "places": 5})

    @task
    def logout(self):
        self.client.get("logout")