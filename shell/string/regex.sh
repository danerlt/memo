#!/usr/bin/env bash

# 下面语法可以检查字符串开头/结尾，是否匹配给定的模式。如果匹配成功，就删除匹配的部分，返回剩下的部分。原始变量不会发生变化
# 匹配模式pattern可以使用*、?、[]等通配符
# {var#正则} 从左到右 最短匹配,然后去掉匹配内容,返回剩余部分
# {var##正则} 从左到右 最长匹配,然后去掉匹配内容,返回剩余部分
# {var%正则}  从右到左 最短匹配,然后去掉匹配内容,返回剩余部分
# {var%%正则} 从右到左 最长匹配,然后去掉匹配内容,返回剩余部分
# 记忆规则 # 表示从左到右匹配，*标识从右到左匹配，一个符号表示最短匹配，两个符号表示最长匹配

url="ai-image.dev.com:8080/neufoundry-private/gateway-outer:origin-feature-sprint0505-e46882a93e1e3dc5d18b747e088b4d8abdb60cc3-20220225112925-V13"
echo "url: ${url}"

# 从左往右匹配，去掉最短匹配内容
echo ${url#*/}
# 从左往右匹配，去掉最长匹配内容
echo ${url##*/}
# 从右往左匹配，去掉最短匹配内容
echo ${url%/*}
# 从右往左匹配，去掉最长匹配内容
echo ${url%%/*}

# 取tag
tag=${url##*:}
echo "tag: ${tag}"

# 取域名
domain=${url%%:*}
echo "domain: ${domain}"

# 取tag前面的部分
prefix=${url%:*}
echo "prefix: ${prefix}"

# 取域名后面的部分
suffix=${url#*/}
echo "suffix: ${suffix}"

# 取项目名
project=${prefix##*/}
echo "project: ${project}"
