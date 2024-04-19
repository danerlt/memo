#!/usr/bin/env bash

old_url="^IMAGE=http://harbor.google.com/python/python:V3"
new_url="#IMAGE=http://harbor.google.com/python/python:V3"


sed -i "s|${old_url}|${new_url}|g" ./test.txt
ret=$?
if [ "$ret" == "0" ]; then
    echo "替换成功"
else
    echo "替换失败"
fi

add_url="IMAGE=http://harbor.google.com/python/python:V4"
sed -i "a|${old_url}|${add_url}|g" ./test.txt
ret=$?
if [ "$ret" == "0" ]; then
    echo "追加成功"
else
    echo "追加失败"
fi