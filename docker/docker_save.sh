#! /bin/bash

# 将docker镜像保存为 项目名.tar.gz文件
# 使用方式 ./docker_save.sh  image_url
# image_url格式为 harbor域名/harbor目录/项目名:分支或者标签-docker哈希值-时间-V版本号
# ai-image.dev.com/neufoundry-private/gateway-outer:origin-feature-sprint0505-e46882a93e1e3dc5d18b747e088b4d8abdb60cc3-20220225112925-V13



function usage() {
    echo "usage: docker_save.sh  iamge_url"
}


if [ $# -ne 1 ]
then
    usage && exit 1
fi

image_url=$1

echo "docker pull ${image_url}"
docker pull $image_url

# 从右到左取old_image_path中取第一个:之前的
image_prefix=${image_url%:*}
echo "image_prefix: $image_prefix"

# 从左往右取第一个/后面的内容
harbor_path=${image_prefix#*/}
echo "harbor_path: $harbor_path"


# 从左往右取最后一个/后面的内容 如果包含_ 取下划线后面的内容
end=${harbor_path##*/}
if [[ $end == *_* ]]
then
    # 从左往右取最后一个 _ 后面的内容
    project_name=${end##*_}
else
    project_name=$end
fi
tar_name=${project_name}.tar

echo "tar file name : $tar_name"

echo "docker save $image_url -o $tar_name"
docker save $image_url -o $tar_name

echo "tar 压缩"
tar czvf ${project_name}.tar.gz $tar_name

echo "执行成功"                                         
