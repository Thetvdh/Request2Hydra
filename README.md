# Request2Hydra

### A program to convert a BurpSuite request capture to a Hydra command

# Usage

```shell
git clone https://github.com/Thetvdh/Request2Hydra
pip3 install -r requirements.txt
python3 main.py -h 
```

# Description
Request2Hydra is a project to simplify using hydras http-post-form functionality.
Instead of having to manually go through a web request, Request2Hydra automatically parses the request and creates a
hydra command.

# Functionality
- Automatically generate hydra command from BurpSuite request
- Automatically detect a failure string
- Detects whether a file or a string has been passed to it

# Issues

If you have any issues with the software please raise an issue.
If you wish to fix it your self, please raise and issue then attach a pull request to it


# Credits

Thanks to these projects for giving me the idea to create this
- [Hydra](https://github.com/vanhauser-thc/thc-hydra)
- [BurpSuite](https://portswigger.net/burp)
