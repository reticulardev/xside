# Tests
Download the Git repository and with the terminal enter the 
project directory.

### unittest
Standard library unit tests can be run as follows
```console
python3 -m unittest discover
```

### coverage
Test coverage can be verified using the "coverage" lib. 
Use pip to install it.
```console
pip3 install --upgrade pip
pip3 install coverage
```
Then run the unit tests using the "coverage" command and then use the 
"report" argument to get the test coverage status.
```console
coverage run -m unittest discover
coverage report -m
```