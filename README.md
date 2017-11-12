This repository contains the source for [my homepage](http://jwhanlon.com),
which is built using [Pelican](https://blog.getpelican.com/).

To get up and running:
```
$ pip install virtualenv
...
$ virtualenv env
$ source env/bin/activate
$ pip -r requirements.txt
...
```

Then, build the website:
```
$ make
...
```

Or, run the development server:
```
$ ./develop_server start
...
$ ./develop_server stop
...
```
Then visit ``http://0.0.0.0:8000``.
