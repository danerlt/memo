#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
"""
@file: min_main.py
@time: 2023-04-20
@desc:  全排列 考虑交叉和剪枝

回溯算法的框架

result = []
def backtrack(路径, 选择列表):
    if 满足结束条件:
        result.add(路径)
        return

    for 选择 in 选择列表:
        做选择
        backtrack(路径, 选择列表)
        撤销选择


算法建模
假设有 4 个点, A, B, C, D 这4个点是固定的  表示选择列表
然后随机生成4个点, a,b,c,d 这4个点是随机生成的  表述深度列表
将这8个点连接起来,要求连线不能交叉

算法思路:

首先定义选择路径列表, [A,B,C,D]
然后定义深度列表, [a,b,c,d]

定义路径列表为空列表, 用来存储走的路径

从根节点开始,
1.第一层: 有4个选择,选择A, B, C , D的任意一个点, 假设是A,然后选择深度列表的第一个点a, 这两个点连线,
  先判断连线的长度是否大于对角线的一半，如果大于就跳过,如果没有大于,再判断这个线段和路径列表中的线段是否有交叉,
  如果有交叉就跳过,如果没有交叉将这个线段加入路径列表,然后进入下一层
2.第二层: 有3个选择,选择B, C, D的任意一个点, 假设是B,然后选择深度列表的第二个点b, 这两个点连线,
  先判断连线的长度是否大于对角线的一半，如果大于就跳过,如果没有大于,再判断这个线段和路径列表中的线段是否有交叉,
  如果有交叉就跳过,如果没有交叉将这个线段加入路径列表,然后进入下一层
3.第三层: 有2个选择,选择C, D的任意一个点, 假设是C,然后选择深度列表的第三个点c, 这两个点连线,
  先判断连线的长度是否大于对角线的一半，如果大于就跳过,如果没有大于,再判断这个线段和路径列表中的线段是否有交叉,
  如果有交叉就跳过,如果没有交叉将这个线段加入路径列表,然后进入下一层
4.第四层: 有1个选择,选择D点,然后选择深度列表的第四个点d, 这两个点连线,
  先判断连线的长度是否大于对角线的一半，如果大于就跳过,如果没有大于,再判断这个线段和路径列表中的线段是否有交叉,
  如果有交叉就跳过,如果没有交叉将这个线段加入路径列表, 说明已经找到了一条解决方案,线段不交叉


"""
import copy
import math
import random
import time

import matplotlib.pyplot as plt

from logutil import creater_logger

logger = creater_logger()


class CrossUtils(object):
    # 组成两条直线段并判断是否相交
    def check_intersection(self, line_1, line_2):
        """

        :param line_1: 线段AB [(x1, y1), (x2, y2)]
        :param line_2: 线段CD [(x3, y3), (x4, y4)]
        :return:
        """
        # 判断两线段是否相交
        # 快速排斥，以l1、l2为对角线的矩形必相交，否则两线段不相交

        p1, p2 = line_1
        p3, p4 = line_2

        if (max(p1.x, p2.x) >= min(p3.x, p4.x)  # 矩形1最右端大于矩形2最左端
                and max(p3.x, p4.x) >= min(p1.x, p2.x)  # 矩形2最右端大于矩形最左端
                and max(p1.y, p2.y) >= min(p3.y, p4.y)  # 矩形1最高端大于矩形最低端
                and max(p3.y, p4.y) >= min(p1.y, p2.y)):  # 矩形2最高端大于矩形最低端

            # 若通过快速排斥则进行跨立实验
            if (self.cross(p1, p2, p3) * self.cross(p1, p2, p4) <= 0
                    and self.cross(p3, p4, p1) * self.cross(p3, p4, p2) <= 0):
                is_intersection = True
            else:
                is_intersection = False
        else:
            is_intersection = False
        return is_intersection

    def cross(self, p1, p2, p3):  # 跨立实验
        x1 = p2.x - p1.x
        y1 = p2.y - p1.y
        x2 = p3.x - p1.x
        y2 = p3.y - p1.y
        return x1 * y2 - x2 * y1

    def is_cross(self, lines):
        flag = False
        for i in range(len(lines)):
            for j in range(len(lines)):
                if i != j:
                    if self.check_intersection(lines[i], lines[j]):
                        flag = True
                        return flag
        return flag

    def is_cross_lines(self, lines, line):
        """判断 line 是否与 lines 里面的线段相交"""
        flag = False
        for i in range(len(lines)):
            if self.check_intersection(lines[i], line):
                flag = True
                return flag
        return flag


class Point(object):
    def __init__(self, x, y, name=None):
        """
        :param x: x坐标
        :param y: y坐标
        :param name: 坐标名称
        """
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        return f"Point(name: {self.name}, {self.x}, {self.y}))"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Group(object):
    def __init__(self, name, points=None, group_point=None):
        """

        :param name: 组名称
        :param points: 组合包含的点列表
        :param group_point: 组合的坐标
        """
        self.name = name
        self.points = points
        self.group_point = group_point

    def __repr__(self):
        return f"Group(name: {self.name}, addr: {self.group_point.name})"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


# 固定点位数量
MAX_POINT = 16
# 每组的数量
GROUP_NUM = 3

# x轴最大值
max_x = 3
# y轴最大值
max_y = 3

x_unit = max_x / 6
y_unit = max_y / 6

# 连线的最大长度，不能超过对角线的一半
max_line_length = ((max_x ** 2 + max_y ** 2) ** 0.5) / 2

# 每次回溯的最大时间 1 秒
max_backtrace_time = 10

#  16个点位图如下
#  M  L  K  J  I
#  N           H
#  O           G
#  P           F
#  A  B  C  D  E
# 所有的固定点位
pa = Point(0, 0, name="A")
pb = Point(1 * x_unit, 0, name="B")
pc = Point(3 * x_unit, 0, name="C")
pd = Point(5 * x_unit, 0, name="D")

pe = Point(max_x, 0, name="E")
pf = Point(max_x, 1 * y_unit, name="F")
pg = Point(max_x, 3 * y_unit, name="G")
ph = Point(max_x, 5 * y_unit, name="H")

pi = Point(max_x, max_y, name="I")
pj = Point(5 * x_unit, max_y, name="J")
pk = Point(3 * x_unit, max_y, name="K")
pl = Point(1 * x_unit, max_y, name="L")

pm = Point(0, 1 * y_unit, name="M")
pn = Point(0, 5 * y_unit, name="N")
po = Point(0, 3 * y_unit, name="O")
pp = Point(0, y_unit, name="P")

all_fix_points = [pa, pb, pc, pd, pe, pf, pg, ph, pi, pj, pk, pl, pm, pn, po, pp]

# 找到一组解的标志
find_path = False
# 已经交叉的线段
loop_num = 0
cross_utils = CrossUtils()


def gen_random_points(point_num=MAX_POINT, repeat_num=0):
    """生成随机坐标
    :param point_num 坐标数量
    :param repeat_num 重复坐标数量
    :return: [(x1, y1), (x2, y2), ...]
    """
    # 生成随机坐标
    points = []
    name = 'a'
    # 生成不重复坐标
    for _ in range(point_num - repeat_num * 2):
        x = round(random.uniform(0, max_x), 1)
        y = round(random.uniform(0, max_y), 1)
        p = Point(x, y, name=str(name))
        name = chr(ord(name) + 1)
        points.append(p)
    return points


def gen_give_list(group_num=None):
    """生成固定点位列表

    从 all_group 中随机选择 group_num 个组合
    :param group_num: 要选择的组合数量
    :return: [(group_list, point_list)...]
    """

    def is_group_points_used(trace, group):
        """
        判断组合中的点是否已经被使用

        比如 group_1 是 (a, b, c), group_2 是 (b, c, d), 如果 trace 是 [(a, b, c)], 那么 group_2 就不能再使用了
        :param trace:
        :param group:
        :return:
        """
        trace_set = set()
        for i in trace:
            trace_set.update(i.points)
        for p in group.points:
            if p in trace_set:
                return True
        return False

    def traceback_group(selects, trace, start_idx=0):
        """回溯组合
        :param selects: 选择列表 这里是组合列表
        :param trace: 路径
        :param start_idx: 起始索引 加上这个是用来去重
        :return:
        """
        # 做判断
        # 路径长度等于 n叉树的高度, 说明找到了一条路径
        if len(trace) == group_num:
            all_trace.append(copy.deepcopy(trace))
            return

        for idx in range(start_idx, len(selects)):
            # 路径已经被走过来,跳过
            if used[idx]:
                continue
            global loop_num
            loop_num += 1
            # 做选择
            group = selects[idx]
            if is_group_points_used(trace, selects[idx]):
                continue
            else:
                trace.append(group)
                # 说明之前走过的路径没有交叉, 向下走
                used[idx] = True
                start_idx = idx + 1
                traceback_group(selects, trace, start_idx=start_idx)
                trace.pop()
                used[idx] = False

    all_trace = []
    # 所有固定的点位
    # 所有可能的组合
    all_groups = [
        Group("group_1", [pa, pb, pc], pb),
        Group("group_2", [pb, pc, pd], pc),
        Group("group_3", [pc, pd, pe], pd),
        Group("group_4", [pd, pe, pf], pe),
        Group("group_5", [pe, pf, pg], pf),
        Group("group_6", [pf, pg, ph], pg),
        Group("group_7", [pg, ph, pi], ph),
        Group("group_8", [ph, pi, pj], pi),
        Group("group_9", [pi, pj, pk], pj),
        Group("group_10", [pj, pk, pl], pk),
        Group("group_11", [pk, pl, pm], pl),
        Group("group_12", [pl, pm, pn], pm),
        Group("group_13", [pm, pn, po], pn),
        Group("group_14", [pn, po, pp], po),
        Group("group_15", [po, pp, pa], pp),
        Group("group_16", [pp, pa, pb], pa),
    ]

    used = [False] * len(all_groups)
    traceback_group(all_groups, [])
    logger.debug(f"len(all_trace): {len(all_trace)}")

    # 合并去掉组合中不需要的的点之后的所有列表
    res = []
    for one_trace in all_trace:
        # 所有组合里面的所有点
        group_all_points_set = set()
        # 所有组合对应需要的点
        group_points_set = set()
        group_names = []
        for group in one_trace:
            group_names.append(group.name)
            group_all_points_set.update(group.points)
            group_points_set.add(group.group_point)

        all_fix_points_set = set(all_fix_points)
        # 这个是所有点减去重复的点再加上组合对应的点 也就是剩下的可能需要的点
        item = (all_fix_points_set - group_all_points_set).union(group_points_set)
        # 这里需要将set转成list 因为set无法通过索引寻找元素
        res.append({
            "group_names": group_names,
            "group_list": list(item),
        })

    logger.debug(f"gen_give_list len(res): {len(res)}")
    return res


def show(lines):
    """画图
    :param lines: [[(x1, y1), (x2, y2)], [(x3, y3), (x4, y4)], ...]
    lines 里面的元素是一个元素, 里面有两个元素, 分别是坐标
    """
    for line in lines:
        point_0 = line[0]
        point_1 = line[1]
        x1, y1 = point_0.x, point_0.y
        x2, y2 = point_1.x, point_1.y
        plt.plot([x1, x2], [y1, y2], 'o-')
    # 展示图形
    plt.grid()
    plt.show()


def show_point(points):
    x_list = []
    y_list = []
    name_list = []

    for point in points:
        x_list.append(point.x)
        y_list.append(point.y)
        name_list.append(point.name)

    plt.scatter(x_list, y_list)
    # 添加标签
    for i, name in enumerate(name_list):
        plt.annotate(name, (x_list[i], y_list[i]))
    # 展示图形
    plt.grid()
    plt.show()


def backtrack(trace, used, depth,
              start_time=None,
              random_points_length=None,
              give_points_length=None, random_points=None,
              give_points=None, group_names=None, result=None):
    """回溯
    # 做判断
    """
    global loop_num
    global find_path
    now = time.time()
    if now - start_time > 1:
        return
    if find_path:
        return
    # 路径长度等于 n叉树的高度, 说明找到了一条路径
    if len(trace) == random_points_length:
        logger.debug(f"找到一个路径,退出回溯, group_name: {group_names}, trace:{trace}")
        result.append(copy.deepcopy(trace))
        find_path = True
        return

    # 做选择
    for idx in range(give_points_length):
        # 路径已经被走过来,跳过
        if used[idx]:
            continue
        loop_num += 1
        give_point = give_points[idx]
        random_point = random_points[depth]  # 每层元素
        cur_line = (random_point, give_point)

        # 判断当前线段是否超过最大长度
        cur_line_length = ((random_point.x - give_point.x) ** 2 + (random_point.y - give_point.y) ** 2) ** 0.5
        if cur_line_length > max_line_length:
            continue

        # 判断是否有交叉
        if cross_utils.is_cross_lines(trace, cur_line):
            # 这里必须用continue, 不能用break, 因为这里是遍历所有的路径, 而不是遍历一条路径
            continue
        else:
            # 说明之前走过的路径没有交叉, 向下走
            trace.append(cur_line)
            used[idx] = True
            depth += 1
            backtrack(trace, used, depth=depth,
                      start_time=start_time,
                      random_points_length=random_points_length,
                      give_points_length=give_points_length,
                      random_points=random_points,
                      give_points=give_points,
                      group_names=group_names,
                      result=result)
            trace.pop()
            depth -= 1
            used[idx] = False


def main_process(repeat_num, point_num):
    t0 = time.time()
    # repeat_num = 0
    random_points = gen_random_points(point_num=point_num, repeat_num=repeat_num)  # 每层元素
    show_point(random_points)
    logger.debug(f"len(random_points) :{len(random_points)},random_points : {random_points}")
    random_points_length = len(random_points)
    give_list = gen_give_list(group_num=repeat_num)

    result = []
    temp_loop = 0
    for give_item in give_list:
        start_time = time.time()
        if find_path:
            break
        one_give_group_names = give_item["group_names"]
        one_give_points = give_item["group_list"]

        temp_loop += 1
        logger.info(f"temp_loop: {temp_loop}, loop_num: {loop_num}, one_give_group_names: {one_give_group_names}")
        trace = []
        used = [False] * len(one_give_points)
        give_points_length = len(one_give_points)
        backtrack(trace, used, depth=0,
                  start_time=start_time,
                  random_points_length=random_points_length,
                  give_points_length=give_points_length,
                  random_points=random_points,
                  give_points=one_give_points,
                  group_names=one_give_group_names,
                  result=result)

    t1 = time.time()
    cost_time = round(t1 - t0, 2)
    is_find = "找到" if result else "未找到"
    logger.info(f"重复组数为: {repeat_num}, 数据点数为: {point_num}, 耗时: {cost_time}秒 {is_find}路径")
    logger.debug(f"loop_num: {loop_num}")
    logger.debug(f"result: {result}")
    # 画图
    for item in result:
        show(item)


def main():
    # show_point(all_fix_points)
    # 重复组数
    repeat_num = 0
    # 数据点数
    point_num = 16
    main_process(repeat_num, point_num)


if __name__ == '__main__':
    main()
