#!/bin/bash
ln -s /usr/local/bin /app/bin
ln -s /usr/local/lib /app/lib
uwsgi --ini uwsgi.ini
