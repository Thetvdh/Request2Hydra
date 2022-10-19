import requests
from bs4 import BeautifulSoup
import re


class RequestHandler:

    def __init__(self, request_file):
        self.request_file = request_file
        self.host = None
        self.request_lines = None
        self.endpoint = None
        self.post_data = {}
        self.setup()

    def extract_post_data(self):
        post_data = self.request_lines[-1]
        post_data = post_data.split("&")
        for data in post_data:
            self.post_data[data.split("=")[0]] = data.split("=")[1]

    def extract_host(self):
        host = self.request_lines[1]
        search = re.search("(?<=Host:.)(?s)(.*$)", host)
        self.host = search.group()

    def get_request_lines(self):
        with open(self.request_file, "r") as request_file:
            self.request_lines = request_file.read().splitlines()

    def setup(self):
        self.get_request_lines()
        self.extract_post_data()
        self.extract_host()
        self.extract_endpoint()
    def __str__(self):
        data = f"\nRequest File: {self.request_file}\n"
        data += "\nRequest Data: "
        data += "\n".join(self.request_lines)
        data += "\n"
        data += f"\nPost Data: {self.post_data}\n"
        data += f"\nHost Data: {self.host}\n"
        data += f"\nEndpoint Data: {self.endpoint}\n"
        return data

    def extract_endpoint(self):
        endpoint = self.request_lines[0]
        endpoint = endpoint.split(" ")
        self.endpoint = endpoint[1]

if __name__ == '__main__':
    handler = RequestHandler("request.txt")
    print(handler)
