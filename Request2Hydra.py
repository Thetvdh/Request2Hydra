import argparse
import os


class Request2Hydra:

    def __init__(self):
        self.args = self.get_cmd_args()
        self.username = self.args.username
        self.password = self.args.password
        self.flags = []
        self.parse_flags()
        self.command = f"hydra {self.flags[0]} {self.username} {self.flags[1]} {self.password}"

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

    def parse_flags(self):
        if os.path.exists(self.args.username):
            self.flags[0] = '-L'
        else:
            self.flags[0] = '-l'
        if os.path.exists(self.args.username):
            self.flags[1] = '-P'
        else:
            self.flags[1] = '-p'


