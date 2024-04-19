#! /usr/bin/env sh

# create logs dir
mkdir -p /app/logs

# start Supervisor with Nginx and uWSGI
exec /usr/local/bin/supervisored -c /app/run/supervisord.conf