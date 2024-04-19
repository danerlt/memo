#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
"""
@desc: 提取pdf文字
"""
import pdfplumber
import os


# 提取一页文字
def extract_text_onepage(filepath, wpage):
    pdf = pdfplumber.open(filepath)
    page = pdf.pages[wpage]
    print(page.extract_text())


# 提取全部文字
def extract_text_allpage(filepath):
    pdf = pdfplumber.open(filepath)

    for page in pdf.pages:
        print(page.extract_text())


if __name__ == '__main__':
    path = os.getcwd()  # 获取当前的操作目录，因为pdf文件放在了当前目录中
    pdf_name = "output.pdf"
    pdf_path = os.path.join(path, pdf_name)  # 文件名

    # extract_text_onepage(pdf_path, 1)
    extract_text_allpage(pdf_path)
