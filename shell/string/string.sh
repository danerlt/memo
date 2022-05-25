#!/usr/bin/env bash

# ${#var} 取字符串长度
# ${var^^} 转为大写
#  ${var,,} 转为小写
# ${var:start:length} 取子串,start从0开始,长度为length

url="ai-image.dev.com:8080/neufoundry-private/gateway-outer:origin-feature-sprint0505-e46882a93e1e3dc5d18b747e088b4d8abdb60cc3-20220225112925-V13"
echo "url: ${url}"

# 取字符串长度
url_length=${#url}
echo "url length: ${url_length}"

upper_url=${url^^}
echo "upper_url: ${upper_url}}"

lower_url=${url,,}
echo "lower_url ${lower_url}"

sub_string=${url:3:5}
echo "sub_string: ${sub_string}"
