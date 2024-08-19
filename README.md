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
$ pre-commit install
```

Build the website:
```
$ make webpack
$ make html
...
$ make validate
```

Run the development server:
```
$ pelican --listen
...
```
Then visit ``http://0.0.0.0:8000`` (or similar).

Regenerate the Pygments styles:
```
pygmentize -S default -f html  > theme/static/css/pygments.css
pygmentize -S monokai -f html  > theme/static/css/pygments-dark.css
```
