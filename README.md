Task 1
======

Requires a python interpreter, tested with Cpython 2.7 and 3.6.

By just running `python bowling/score.py` the included tests are executed.

Alternatively, the scores of a game can be given as command line arguments,
where the rolls of a frame are separated by a comma and frames are separated by
a space. Multiple games can be entered after another by quoting the string for
each game.

Example:

`python bowling/score.py "10,0 10,0, 10,0 10,0 10,0 10,0 10,0 10,0 10,0 10,10,10"


Task 2
======

Requires ansible, ssh access to localhost and a docker installation on localhost.
Tested with Ansible 2.5.1, Docker 17.05.0-ce.

To use a different host just change the `haproxy/inventory` file.

To run the ansible playbook use the following command:

`ansible-playbook -i haproxy/inventory  haproxy/hello.yaml`

If all goes well, the URL http://localhost:8000/hello should return the desired
content.
