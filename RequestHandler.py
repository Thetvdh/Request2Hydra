import requests
import re


class RequestHandler:

    def __init__(self, request_file):
        self.request_file = request_file
        self.host = None
        self.port = None
        self.request_lines = None
        self.endpoint = None
        self.post_data = {}
        self.url = None
        self.setup()

    def extract_post_data(self):
        post_data = self.request_lines[-1]
        post_data = post_data.split("&")
        for data in post_data:
            self.post_data[data.split("=")[0]] = data.split("=")[1]

    def extract_host(self):
        host = self.request_lines[1]
        search = re.search("(?<=Host:.)(?s)(.*$)", host)
        host = search.group()
        host = host.split(":")
        print(host)
        try:
            self.host = host[0]
            self.port = host[1]
        except Exception:
            self.host = host[0]
            self.port = None



    def get_request_lines(self):
        with open(self.request_file, "r") as request_file:
            self.request_lines = request_file.read().splitlines()

    def setup(self):
        self.get_request_lines()
        self.extract_post_data()
        self.extract_host()
        self.extract_endpoint()
        self.url = f"http://{self.host}" + f":{self.port}" if self.port is not None else ""
        self.url += self.endpoint

    def __str__(self):
        data = f"\nRequest File: {self.request_file}\n"
        data += "\nRequest Data: "
        data += "\n".join(self.request_lines)
        data += "\n"
        data += f"\nPost Data: {self.post_data}\n"
        data += f"\nHost Data: {self.host}\n"
        data += f"\nEndpoint Data: {self.endpoint}\n"
        data += f"\nUrl: {self.url}\n"
        return data

    def extract_endpoint(self):
        endpoint = self.request_lines[0]
        endpoint = endpoint.split(" ")
        self.endpoint = endpoint[1]

    def get_failure_message(self):
        get_resp = requests.get(self.url)
        post_resp = requests.post(self.url, self.post_data)
        get_resp_list = get_resp.text.splitlines()
        post_resp_list = post_resp.text.splitlines()

        difference = list(set(get_resp_list) ^ set(post_resp_list))[0]
        difference = re.sub("<.*?>", "", difference.lstrip())
        return difference


if __name__ == '__main__':
    handler = RequestHandler("request.txt")
    print(handler)
    handler.get_failure_message()
