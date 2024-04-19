#!/bin/bash

# create logs dis
mkdir -p /app/logs

# start supervisord
exec /usr/local/bin/supervisord -c /app/supervisord.conf
