![Build](https://github.com/jameshanlon/homepage/actions/workflows/build.yml/badge.svg)

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

Build the website:
```
$ make
...
$ make validate
```

Run the development server:
```
$ pelican --listen
...
```
Then visit ``http://0.0.0.0:8000``.
