#! /bin/bash

# 将docker镜像保存为 项目名.tar.gz文件
# 使用方式 ./docker_save.sh  image_url
# image_url格式为 harbor域名/harbor目录/项目名:分支或者标签-docker哈希值-时间-V版本号
# ai-image.dev.com/neufoundry-private/gateway-outer:origin-feature-xy-Sprint1216-docker-e46882a93e1e3dc5d18b747e088b4d8abdb60cc3-20220225112925-V13

# cd /tmp

image_url=$1

echo "docker pull ${image_url}"
docker pull $image_url

array=(${image_url//:/ })
prefix=${array[0]}
array2=(${prefix//// })
image_name=${array2[-1]}
echo "image_name: $image_name"

tar_name=${image_name}.tar

echo "tar name: $tar_name"

echo "docker save $image_url -o $tar_name"
docker save $image_url -o $tar_name

echo "tar 压缩"
tar zcvf ${image_name}.tar.gz $tar_name

echo "执行成功"                                         
