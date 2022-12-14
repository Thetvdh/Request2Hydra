import argparse
import os
from RequestHandler import RequestHandler


class Request2Hydra:

    """
    # __init__()
    # Sets up all variables to use in this class.
    """
    def __init__(self):
        self.args = self.get_cmd_args()
        self.request_handler = RequestHandler(self.args.rfile)  # Creates the request handler object
        self.username = self.args.username
        self.password = self.args.password
        self.host = self.request_handler.host
        self.port = self.request_handler.port
        self.endpoint = self.request_handler.endpoint
        self.post_data = self.request_handler.post_data.keys()
        self.parsed_post_data = self.parse_post_data()
        self.failure = self.request_handler.get_failure_message()
        self.flags = []
        self.string_flags = ""
        self.parse_flags()
        self.command = f'hydra {self.flags[0]} {self.username} {self.flags[1]} {self.password} {self.host} ' \
                       f'http-post-form "{self.endpoint}:{self.parsed_post_data}:{self.failure}" -V {self.string_flags}' \


    def __str__(self):
        return "\n\n\n" + self.command + "\n\n"

    # get command line arguments
    def get_cmd_args(self):
        parser = argparse.ArgumentParser(description="Convert a web intercept to a hydra command")
        parser.add_argument('-r', '--request', dest="rfile", required=True, help="The file containing the web request")
        parser.add_argument('-u', '--user', dest="username", required=True, help="either a string username or a file "
                                                                                 "containing usernames")
        parser.add_argument('-p', '--password', dest="password", required=True,
                            help="either a string password or a file "
                                 "containing passwords")

        return parser.parse_args()

    """
    # parse_flags()
    # Checks if the username and password supplied are directories or files. 
    # Sets the correct flag accordingly
    # Loops through any other flags in the array and adds them to a string version of the array
    # This is then added to the end of the command
    """
    def parse_flags(self):
        if os.path.exists(self.args.username):
            self.flags.append("-L")
        else:
            self.flags.append("-l")
        if os.path.exists(self.args.password):
            self.flags.append("-P")
        else:
            self.flags.append("-p")
        if self.port is not None:
            self.flags.append(f"-s {self.port}")

        for i in range(2, len(self.flags)):
            self.string_flags = "".join(self.flags[i])

    """
    # parse_post_data()
    # Parses the post data gathered from the RequestHandler()
    # checks to see if the post data is a username or password and if it is applies the special hydra syntax
    # Otherwise it just adds it to the end
    """
    def parse_post_data(self):
        output = ""
        for item in self.post_data:
            if "user" in item:
                output += f"{item}=^USER^"
            elif "pass" in item:
                output += f"{item}=^PASS^"
            else:
                output += item
            output += "&"

        if output[-1] == '&':  # Removes trailing ampersand leftover from the for loop
            output = output[:-1]
        return output
