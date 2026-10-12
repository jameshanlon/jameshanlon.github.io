PY?=python
BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/output
PORT?=8000

all: html

html:
	$(PY) -m ssg -o $(OUTPUTDIR) build

serve:
	$(PY) -m ssg -o $(OUTPUTDIR) serve -p $(PORT) --watch

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

manifest:
	$(PY) tools/make_manifest.py $(OUTPUTDIR)

test:
	$(PY) -m pytest -v

.PHONY: all html serve clean manifest test
