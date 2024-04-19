#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt
@file: chrome_bookmarks_to_md.py 
@time: 2022-09-22
@contact: danerlt001@gmail.com
@desc: Chrome书签装成Markdown文件
"""

import os
import sys
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    is_a = False
    is_h3 = False
    links = []
    cur_tag_key = ''
    cur_tag_value = ''

    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        # print "Encountered the beginning of a %s tag" % tag
        if tag == 'a':
            self.is_a = True
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.cur_tag_value = value
        else:
            self.is_h3 = True

    def handle_data(self, data):
        if self.is_a:
            self.cur_tag_key = data
        elif self.is_h3:
            self.cur_tag_key = data
            self.cur_tag_value = 'h3'

    def handle_endtag(self, tag):
        if tag == 'a' or tag == 'h3':
            self.is_a = False
            self.is_h3 = False
            if self.cur_tag_key == '' and self.cur_tag_value == '':
                pass
            else:
                self.links.append([self.cur_tag_key, self.cur_tag_value])
                self.cur_tag_key = ''
                self.cur_tag_value = ''


def parse_args():
    """参数解析"""
    if len(sys.argv) <= 1:
        raise Exception("参数错误,没有指定书签文件路径")
    book_marks_path = sys.argv[1]
    return book_marks_path


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        return content


def append_file(file_path, content):
    """向文件追加内容"""
    with open(file_path, "a+", encoding="utf-8") as f:
        f.write(content)


def main():
    book_marks_path = parse_args()
    file_content = read_file(book_marks_path)
    hp = MyHTMLParser()
    hp.feed(file_content)
    hp.close()

    book_md_file = "book_marks.md"
    try:
        os.remove(book_md_file)
    except Exception:
        pass
    append_file(book_md_file, "# Chrome书签\n\n")
    for word in hp.links:
        if word[1] == 'h3':
            append_file(book_md_file, '##' + word[0] + '\n\n')
            print(word[0] + '\n')
        else:
            append_file(book_md_file, '- [' + word[0] + '](' + word[1] + ')\n\n')
            print('- [' + word[0] + '](' + word[1] + ')\n')


if __name__ == '__main__':
    main()
