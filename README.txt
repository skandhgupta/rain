to setup (does not require sudo, as it makes no changes outside the current dir)
$ ./configure
$ make

whenever you're starting a session:
$ source activate


Advanced:
---------

after installing a package in the virtualenv:
(ps: make sure that the virtualenv is active)
$ pip freeze >dep/requirements.txt
