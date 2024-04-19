#!/bin/bash


ab -n 10000 -c 1000 -T "application/json" -p data.json http://127.0.0.1:5000/embed