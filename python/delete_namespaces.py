#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
"""
@desc:  批量删除k8s命名空间 删除命名空间的时候会卡在Terminating状态,需要手动调用接口删除


参考链接: https://support.huaweicloud.com/cce_faq/cce_faq_00277.html

调用之前必须先执行
kubectl proxy --address='0.0.0.0' --port=8081


用法:

python delete_namespaces.py namespaces.txt


namespaces.txt 格式如下,每一行一个命名空间
aaa
bbb
ccc
"""
import json
import os
import sys

import requests


def can_delete_namespace(namespace):
    cmd = f"kubectl get ns {namespace}"
    code = os.system(cmd)
    if int(code) == 0:
        return True
    else:
        return False


def get_namespaces_by_file(path):
    if not os.path.exists(path):
        raise Exception(f"No such file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")
        namespaces = []
        for line in lines:
            line = line.strip()
            namespaces.append(line)
        return namespaces


def delete_namespace(namespace):
    print(f"begin delete namespace: {namespace}")
    tmp_path = "/tmp/delete_namespaces"
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    json_path = os.path.join(tmp_path, f"{namespace}.json")
    cmd = f"kubectl  get ns {namespace}  -o json > {json_path}"
    print(f"execute command: {cmd}")
    os.system(cmd)

    url = f"http://127.0.0.1:8081/api/v1/namespaces/{namespace}/finalize"
    headers = {"Content-Type": "application/json"}
    with open(json_path, "r", encoding="utf-8") as f:
        namespace_dict = json.load(f)
        spec = namespace_dict.get("spec", {})
        if spec and "finalizers" in spec:
            del spec["finalizers"]
            namespace_dict["spec"] = spec
        print(f"http put url: {url}, data: namespace_dict: {namespace_dict}")
        res = requests.put(url, headers=headers, data=json.dumps(namespace_dict))
        print(f"response status_code: {res.status_code}")
        print(f"response content: {res.content}")
        print(f"success delete namespace: {namespace}")


def main():
    namespaces_txt = sys.argv[1]
    namespaces = get_namespaces_by_file(namespaces_txt)
    for namespace in namespaces:
        if namespace and can_delete_namespace(namespace):
            delete_namespace(namespace)


if __name__ == '__main__':
    main()
