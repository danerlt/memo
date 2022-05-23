#!/usr/bin/env bash

new_url="#IMAGE=http://harbor.google.com/python/python:V3"

new_url2=$(echo $new_url | sed "s|/|\\\/|g")

echo "$new_url2"

add_url="IMAGE=http://harbor.google.com/python/python:V4"

num=$(sed -n /"${new_url2}"/= ./test.txt)
echo "$num"

#
sed -i "${num} a \\${add_url}" ./test.txt
ret=$?
if [ "$ret" == "0" ]; then
  echo "追加成功"
else
  echo "追加失败"
fi
