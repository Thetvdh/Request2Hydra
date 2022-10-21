import sys

import requests
import re


class RequestHandler:
    """
    # __init__()
    # Sets up the required variables for use in the program. setup() populates all these variables
    """

    def __init__(self, request_file):
        self.request_file = request_file
        self.host = None
        self.port = None
        self.request_lines = None
        self.endpoint = None
        self.post_data = {}
        self.url = None
        self.setup()

    """
    # extract_post_data()
    # takes the last line from a burp suite request. This contains the post data. 
    # In current state program assumes the file is a POST request.
    # Places the post data into a dictionary, splitting by the "&" sign to determine each key:value pair and the = sign
    # To determine what is the key and what is the value
    """

    def extract_post_data(self):
        post_data = self.request_lines[-1]
        post_data = post_data.split("&")
        for data in post_data:
            self.post_data[data.split("=")[0]] = data.split("=")[1]

    """
    # extract_host()
    # Uses regex to extract the host and port, if supplied, from the request. Looks at the second line in the request
    # which looks like
    # Host: {host here}
    # Splits by the ':' character
    # Tries to enter them into variables but if the list index is out of range then the port is set to None
    """

    def extract_host(self):
        host = self.request_lines[1]
        search = re.search("(?<=Host:.)(?s)(.*$)", host)
        host = search.group()
        host = host.split(":")
        try:
            self.host = host[0]
            self.port = host[1]
        except IndexError:
            self.host = host[0]
            self.port = None
    """
    # get_request_lines()
    # Simple function to split the request file into individual lines for manipulation. Stored in a list
    """
    def get_request_lines(self):
        with open(self.request_file, "r") as request_file:
            self.request_lines = request_file.read().splitlines()

    """
    # setup()
    # called in __init__()
    # Runs all the necessary methods to populate the init variables.
    """
    def setup(self):
        self.get_request_lines()
        self.extract_post_data()
        self.extract_host()
        self.extract_endpoint()
        self.url = f"http://{self.host}"
        if self.port is not None:
            self.url += f":{str(self.port)}"
        self.url += self.endpoint

    """
    Debugging overloaded __str__(). Never hit when run from main.py
    """
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

    """
    # extract_endpoint()
    # looks at the first line in the request, should look something like this.
    # POST /endpoint HTTP/1.1
    # Extracts just the endpoint for use in the URL. 
    """
    def extract_endpoint(self):
        endpoint = self.request_lines[0]
        endpoint = endpoint.split(" ")
        self.endpoint = endpoint[1]

    """
    # Attempts to automatically get the failure message from the site. 
    # If it is unable to connect for some reason then an option is given to manually enter the failure string
    # 
    """
    def get_failure_message(self):
        try:
            get_resp = requests.get(self.url)  # Sends get request
            post_resp = requests.post(self.url, self.post_data)  # Sends post request
            get_resp_list = get_resp.text.splitlines()  # splits the get request into individual lines
            post_resp_list = post_resp.text.splitlines()  # splits the post request into individual lines

            # Compares the difference between the two requests. Extracts the difference.
            difference = list(set(get_resp_list) ^ set(post_resp_list))[0]
            difference = re.sub("<.*?>", "", difference.lstrip())  # Removes any leading chars and any HTML tags
            difference = difference.rstrip()  # Removes any trailing chars
            return difference
        except requests.exceptions.ConnectionError:
            choice = input("Unable to automatically detect fail string. Supply string manually? Y/N: ").upper()
            if choice == 'Y':
                return input("Enter the string: ")
            else:
                print("Unable to complete program. Exiting...")
                sys.exit()

