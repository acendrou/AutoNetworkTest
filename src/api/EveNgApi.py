import requests
from evengsdk.client import EvengClient


class EveNgApi:

    def __init__(self, url: str, username: str, password: str):
        self.url = "http://" + url
        self.username = username
        self.password = password
        self.client = EvengClient(url, log_file="log.txt", ssl_verify=False)
        self.client.set_log_level("DEBUG")
        self.client.login(username=self.username, password=password)

    def lab(self, lab_name: str):
        lab = self.client.api.get_lab(path=lab_name)
        print(lab)

    def node(self, lab_name, node_name):
        node = self.client.api.get_node_by_name(path=lab_name, name=node_name)
        print(node)
        return node

    def _authenticate(self):
        api_url = "/api/auth/login"
        url = self.url + api_url
        r = requests.get(
            url,
            params="{"
            + f'"username": {self.username}, "password": {self.password}'
            + "}",
        )
        print(r.status_code)


def test():
    url = "192.168.1.129"
    username = "admin"
    password = "eve"
    lab = "TEST"
    api = EveNgApi(url=url, username=username, password=password)
    api.lab(lab_name=lab)
    api.node(lab_name=lab, node_name="VyOS-1")


if __name__ == "__main__":
    test()
