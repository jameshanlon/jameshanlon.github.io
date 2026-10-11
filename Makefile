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

all: html

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

REFERENCE=$(BASEDIR)/reference

manifest:
	$(PY) tools/make_manifest.py $(OUTPUTDIR)

reference:
	rm -rf $(REFERENCE)
	$(PELICAN) $(INPUTDIR) -o $(REFERENCE) -s $(CONFFILE) $(PELICANOPTS)

diff:
	diff -r -x thumbs $(REFERENCE) $(OUTPUTDIR)

test:
	pytest -v

.PHONY: html clean regenerate serve validate manifest reference diff test
