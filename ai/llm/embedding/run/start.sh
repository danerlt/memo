#! /usr/bin/env sh

# create logs dis
mkdir -p /app/logs

# Start Supervisor, with Nginx and uWSGI
exec /usr/local/bin/supervisord -c /app/run/supervisord.conf