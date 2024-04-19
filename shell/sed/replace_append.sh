#!/usr/bin/env bash

old_url="IMAGE=http://harbor.google.com/python/python:V3"
new_url="IMAGE=http://harbor.google.com/python/python:V4"

replace_to_url="#${old_url}\n${new_url}"

sed -i "s|^${old_url}|${replace_to_url}|g" ./test.txt
ret=$?
if [ "$ret" == "0" ]; then
    echo "替换成功"
else
    echo "替换失败"
fi
