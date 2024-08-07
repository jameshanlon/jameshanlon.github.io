PY?=python
PELICAN?=pelican
PELICANOPTS=--verbose

BASEDIR=`pwd`
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

all: webpack html

webpack:
	npm install
	npx webpack

html:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

regenerate:
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

serve:
ifdef PORT
	pelican -r --listen -b 0.0.0.0 -p $(PORT)
else
	pelican -r --listen -b 0.0.0.0
endif

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

validate: html
	html5validator --root $(OUTPUTDIR)

.PHONY: html help clean regenerate serve
