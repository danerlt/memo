#! /usr/bin/env bash

function usage() {
  echo "usage: bash replace_test.sh file_path var_name var_value"
}

if [ $# -ne 3 ]; then
  usage && exit 1
fi

function replace() {
  ###########################################
  # 替换Image
  # $1 为 需要替换的文件
  # $2 为 需要被替换的变量名
  # $3 为 需要替换成的变量值
  ###########################################

  if [ $# != 3 ]; then
    echo "replace函数参数错误,参数必须为三个,传递参数为: $*"
    exit 1
  fi

  local file_path=$1
  echo "开始替换${file_path}"
  if [ ! -f ${file_path} ]; then
    echo "file not found"
    exit 2
  fi

  local name=$2
  local value=$3
  echo "替换${name}的值为: ${value}"

  is_exist_name=$(cat <${file_path} | grep ${name})
  if [ "$is_exist_name" != "0" ]; then
    echo "变量名${name}不存在"
    exit 3
  fi

  replace_value="${name} = \"${value}\""
  echo "replace_value: ${replace_value}"

  is_success=$(sed -i "s|^${name}.*|${replace_value}|g" ${file_path})
  if [ "$is_success" == "0" ]; then
    echo "替换${name}成功"
  else
    echo "替换${name}失败"
  fi
}

# 替换image_list.sh
file_path=$1
var_name=$2
var_value=$3
replace ${file_path} ${var_name} ${var_value}
