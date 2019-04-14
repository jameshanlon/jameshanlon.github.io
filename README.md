This repository contains the source for [my homepage](http://jameswhanlon.com),
which is built using [Pelican](https://blog.getpelican.com/).

To get up and running:
```
$ pip install virtualenv
...
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
...
```

Then, build the website:
```
$ make
...
```

Or, run the development server:
```
$ pelican --listen
...
```
Then visit ``http://0.0.0.0:8000``.
