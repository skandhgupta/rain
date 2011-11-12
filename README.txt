to setup (does not require sudo, as it makes no changes outside the current dir)
$ ./configure
$ make

whenever you're starting a session:
$ source activate

after that, you can do:
- starting the master:
  $ python src/master.py etc/master.config
- starting workers:
  $ python src/worker.py etc/worker.config
- if you want to start multiple workers on the same machine, you'll need
   to override the port # on the command line
  $ python src/worker.py etc/worker.config --port 5566

For convenience, all this is wrapped up by a helper script that does not
require you to do a 'source activate' beforehand
  $ python src/cluster.py etc/cluster.config --start


Advanced:
---------

after installing a package in the virtualenv:
(ps: make sure that the virtualenv is active)
$ pip freeze >dep/requirements.txt
