#! /bin/bash

# 将docker镜像保存为 项目名.tar.gz文件
# 使用方式 ./docker_save.sh  image_url
# image_url格式为 harbor域名/harbor目录/项目名:分支或者标签-docker哈希值-时间-V版本号
# ai-image.dev.com/dirname/xxxx_projectName:origin-feature-branch-xxxxxxxxxxx-20220225112925-Vxxx

function usage() {
  echo "usage: docker_save.sh  image_url"
}

if [ $# -ne 1 ]; then
  usage && exit 1
fi

image_url=$1

# 从右到左最短匹配:*,去掉匹配内容
image_prefix=${image_url%:*}
echo "image_prefix: ${image_prefix}"

# 从左往右最长匹配*/,去掉匹配内容
end=${image_prefix##*/}
echo "end: ${end}"

# 如果包含_ 取下划线后面的内容
if [[ $end == *_* ]]; then
  # 从左往右最长匹配*_去掉匹配内容
  project_name=${end##*_}
else
  project_name=$end
fi
echo "project_name: ${project_name}"

echo "docker pull ${image_url}"
ret=$(docker pull "${image_url}")
if [ "$ret" != "0" ]; then
  echo "docker pull 失败"
  exit 1
fi

tar_name=${project_name}.tar
echo "tar file name : $tar_name"
if [ -n "$tar_name" ]; then
  echo "docker save ${image_url} -o ${tar_name}"
  docker save "${image_url}" -o "${tar_name}"
  echo "docker save成功"
fi

if [ -f "$tar_name" ]; then
  echo "tar 压缩"
  tar czvf "${project_name}.tar.gz" "$tar_name"
  echo "tar 压缩成功"
fi

echo "结束"
