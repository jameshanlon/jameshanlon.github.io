#!/usr/bin/env bash
source env/bin/activate
make
pelican --listen
