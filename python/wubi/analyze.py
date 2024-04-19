#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
"""
@file: analyze.py 
@time: 2022-10-06
@desc: 分析五笔和小鹤音形
"""

import os
import opencc

# 繁体转简体
converter = opencc.OpenCC('t2s.json')

current_dir = os.path.dirname(os.path.abspath(__file__))
wubi_98_path = os.path.join(current_dir, "98.txt")
wubi_86_path = os.path.join(current_dir, "86.txt")

xiaohe_path = os.path.join(current_dir, "xiaohe.txt")
xiaohe_convert_path = os.path.join(current_dir, "xiaohe_convert.txt")


def convert_xiaohe():
    result = {}
    with open(xiaohe_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                try:
                    word, code = line.split("\t")
                except Exception as e:
                    print(line)
                if len(code) < 4:
                    code += "_"

                i = 1
                temp_code = code
                while temp_code in result:
                    i += 1
                    temp_code = code + str(i)
                code = temp_code
                result[code] = word

    with open(xiaohe_convert_path, "w", encoding="utf-8") as f2:
        for code, word in result.items():
            f2.write(f"{word}\t{code}\n")


def read_map_table(path):
    """读取码表，返回字典

    :return dict   key: 编码   value: 汉字或词组
    """
    result = {}
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line:
                word, code = line.split("\t")
                word = word.strip()
                code = code.strip()
                result[code] = word

        return result


def is_simplified_chinese(word):
    """是否是是简体字
    :param word: 单字
    :return True: 是简体字 False：是繁体字
    """
    # converter.convert(word) 表示繁体字转成简体字
    # 繁体字 调用这个之后变成简体字
    return word == converter.convert(word)


def statistics(map, map_type="98五笔"):
    """统计码表"""
    single_word = []  # 单字
    simplified_chinese_word = []  # 简体字
    traditional_chinese_word = []  # 繁体字
    two_word_phrase = []  # 两字词组
    three_word_phrase = []  # 三字词组
    multi_word_phrase = []  # 多字词组
    sigle_brief = []  # 一级简码
    two_brief = []  # 二级简码
    three_brief = []  # 三级简码
    repeat = []  # 重码
    sigle_repeat = []  # 单字重码
    sc_repeat = []  # 简体字重码
    tc_repeat = []  # 繁体字重码
    for code, word in map.items():
        word_len = len(word)
        code_len = len(code)
        if word_len == 1:
            single_word.append(word)
            if is_simplified_chinese(word):
                simplified_chinese_word.append(word)
            else:
                traditional_chinese_word.append(word)
        elif word_len == 2:
            two_word_phrase.append(word)
        elif word_len == 3:
            three_word_phrase.append(word)
        else:
            multi_word_phrase.append(word)

        if code.endswith("_"):
            if code_len == 2:
                sigle_brief.append(word)
            elif code_len == 3:
                two_brief.append(word)
            elif code_len == 4:
                three_brief.append(word)

        if code_len > 4:
            repeat.append(word)
            if word_len == 1:
                sigle_repeat.append(word)
                if word in simplified_chinese_word:
                    sc_repeat.append(word)
                else:
                    tc_repeat.append(word)

    print(f"{map_type}单字数量: {len(single_word)}")
    print(f"{map_type}简体字数量: {len(simplified_chinese_word)}")
    print(f"{map_type}繁体字数量: {len(traditional_chinese_word)}")
    print(f"{map_type}两字词组数量: {len(two_word_phrase)}")
    print(f"{map_type}三字词组数量: {len(three_word_phrase)}")
    print(f"{map_type}多字词组数量: {len(multi_word_phrase)}")
    print(f"{map_type}一级简码数量: {len(sigle_brief)}")
    print(f"{map_type}二级简码数量: {len(two_brief)}")
    print(f"{map_type}三级简码数量: {len(three_brief)}")
    print(f"{map_type}重码数量: {len(repeat)}")
    print(f"{map_type}码表总数量: {len(map)}")
    print(f"{map_type}重码率: {round(len(repeat) / len(map) * 100, 2)}%")
    print(f"{map_type}单字重码数量: {len(sigle_repeat)}")
    print(f"{map_type}简体字重码数量: {len(sc_repeat)}")
    print(f"{map_type}繁体字重码数量: {len(tc_repeat)}")
    print(f"{map_type}单字重码率: {round(len(sigle_repeat) / len(single_word) * 100, 2)}%")
    print(f"{map_type}简体字重码率: {round(len(sc_repeat) / len(simplified_chinese_word) * 100, 2)}%")
    print()


def main():
    convert_xiaohe()
    map_xiaohe = read_map_table(xiaohe_convert_path)
    map_98 = read_map_table(wubi_98_path)
    map_86 = read_map_table(wubi_86_path)
    statistics(map_xiaohe, map_type="小鹤音形")
    statistics(map_98, map_type="98五笔")
    statistics(map_86, map_type="86五笔")


if __name__ == '__main__':
    main()
