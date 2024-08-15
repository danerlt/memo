import asyncio
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from multiprocessing import Process
from threading import Thread
from time import perf_counter

import aiohttp
import pytest
import requests

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def fib(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def cpu_bound():
    # CPU bound 型任务
    # 调用fib计算斐波那契数
    n = 30
    return fib(n)


def request(n):
    # 请求百度 返回前n个text
    response = requests.get("https://www.baidu.com/")
    res = response.text[0:n]
    return res


async def async_request(n):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.baidu.com/") as response:
            text = await response.text()
            res = text[0:n]
            return res


async def async_request_optimize(session, url, n):
    async with session.get(url) as response:
        text = await response.text()
        res = text[0:n]
        return res


def io_bound():
    # io bound 型任务 同步类型
    n = 100
    return request(n)


async def async_io_bound():
    # io bound 型任务 异步类型
    n = 100
    return await async_request(n)


def single_task(func, *args, **kwargs):
    # 执行一次
    start = perf_counter()
    res = func(*args, **kwargs)
    print(res)
    end = perf_counter()
    cost = round(end - start, 2)
    print(f"single {func.__name__}() cost {cost} second")


async def async_single_task(func, *args, **kwargs):
    # 执行一次
    start = perf_counter()
    res = await func(*args, **kwargs)
    print(res)
    end = perf_counter()
    cost = round(end - start, 2)
    print(f"single {func.__name__}() cost {cost} second")


def for_task(func, *args, **kwargs):
    # for 循环执行多次
    for_loop = 100
    res = []
    start = perf_counter()
    for _ in range(for_loop):
        res.append(func(*args, **kwargs))
    end = perf_counter()
    cost = round(end - start, 2)
    print(f"{func.__name__}() for loop {for_loop} count, cost {cost} second")


async def async_for_task(loop_count, func, *args, **kwargs):
    # for 循环执行多次 异步
    start = perf_counter()
    tasks = []
    for _ in range(loop_count):
        tasks.append(func(*args, **kwargs))
    res = await asyncio.gather(*tasks)
    print(res)
    end = perf_counter()
    cost = round(end - start, 2)
    print(f"{func.__name__}() async for loop {loop_count} count, cost {cost} second")


async def async_for_task_optimize(loop_count, func, *args, **kwargs):
    # for 循环执行多次 异步 优化版本
    start = perf_counter()
    tasks = []
    async with aiohttp.ClientSession() as session:
        for _ in range(loop_count):
            tasks.append(async_request_optimize(session, "https://www.baidu.com/", 100))
        res = await asyncio.gather(*tasks)
        print(res)
    end = perf_counter()
    cost = round(end - start, 2)
    print(f"async_request_optimize() async for loop {loop_count} count, cost {cost} second")


def multi_thread_tasks(thread_num, func, *args, **kwargs):
    # 多线程方式 这个没有返回值
    start = perf_counter()
    threads = []
    for _ in range(thread_num):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    end = perf_counter()
    cost = round(end - start, 2)
    # 5 thread count, fib(35) cost 28.17 second
    print(f"{func.__name__}() execute {thread_num} thread, cost {cost} second")


def multi_process_tasks(func, *args, **kwargs):
    # 多进程方式，这个没有返回值
    process_num = 100
    start = perf_counter()
    process_list = []
    for _ in range(process_num):
        process = Process(target=func, args=args, kwargs=kwargs)
        process_list.append(process)
        process.start()

    for process in process_list:
        process.join()
    end = perf_counter()
    cost = round(end - start, 2)
    # 5 process count, fib(35) cost 9.97 second
    print(f"{func.__name__}() execute {process_num} process, cost {cost} second")


def multi_thread_tasks_with_concurrent(max_work, task_num, func, *args, **kwargs):
    # 多线程方式 这个有返回值
    # 这种方式跟直接使用多线程方式效果一样，但是使用concurrent可以获取返回值
    start = perf_counter()
    res = []
    with ThreadPoolExecutor(max_workers=max_work) as executor:
        tasks = []
        for _ in range(task_num):  # 模拟多个任务 并发执行
            future = executor.submit(func, *args, **kwargs)
            tasks.append(future)

        for future in as_completed(tasks):  # 获取结果
            res.append(future.result())
    print(res)
    end = perf_counter()
    cost = round(end - start, 2)
    # 5 thread with concurrent, fib(35) cost 28.24 second
    print(f"{max_work} thread execute {task_num} {func.__name__}() task with concurrent, cost {cost} second")


def multi_process_tasks_with_concurrent(max_work, task_num, func, *args, **kwargs):
    # 多进程方式 这个有返回值
    # 这种方式跟直接使用多线程方式效果一样，但是使用concurrent可以获取返回值
    start = perf_counter()
    res = []
    with ProcessPoolExecutor(max_workers=max_work) as executor:
        tasks = []
        for _ in range(task_num):  # 模拟多个任务 并发执行
            future = executor.submit(func, *args, **kwargs)
            tasks.append(future)

        for future in as_completed(tasks):  # 获取结果
            res.append(future.result())
    print(res)
    end = perf_counter()
    cost = round(end - start, 2)
    # 5 thread with concurrent, fib(35) cost 28.24 second
    print(f"{max_work} process execute {task_num} {func.__name__}() task with concurrent, cost {cost} second")


def test_single_cpu_bound():
    # single cpu_bound() cost 0.48 second
    single_task(cpu_bound)


def test_single_io_bound():
    # single io_bound() cost 0.18 second
    single_task(io_bound)


@pytest.mark.asyncio
async def test_single_async_io_bound():
    # single async_io_bound() cost 0.23 second
    await async_single_task(async_io_bound)


def test_for_cpu_bound():
    # cpu_bound() for loop 100 count, cost 50.37 second
    for_task(cpu_bound)


def test_for_io_bound():
    # io_bound() for loop 100 count, cost 18.73 second
    for_task(io_bound)


@pytest.mark.asyncio
async def test_for_async_io_bound_100_count():
    # async_io_bound() async for loop 100 count, cost 0.65 second
    await async_for_task(100, async_io_bound)


@pytest.mark.asyncio
async def test_for_async_io_bound_1000_count():
    # async_io_bound() async for loop 1000 count, cost 6.16 second
    await async_for_task(1000, async_io_bound)


@pytest.mark.asyncio
async def test_for_async_io_bound_optimize_100_count():
    # async_request_optimize() async for loop 100 count, cost 0.8 second
    await async_for_task_optimize(100, async_io_bound)


@pytest.mark.asyncio
async def test_for_async_io_bound_optimize_1000_count():
    # async_request_optimize() async for loop 1000 count, cost 1.45 second
    await async_for_task_optimize(1000, async_io_bound)


@pytest.mark.asyncio
async def test_for_async_io_bound_optimize_5000_count():
    # async_request_optimize() async for loop 5000 count, cost 5.68 second
    await async_for_task_optimize(5000, async_io_bound)


def test_multi_thread_cpu_bound():
    # cpu_bound() execute 100 thread, cost 59.7 second
    multi_thread_tasks(100, cpu_bound)


def test_multi_thread_io_bound_100_count():
    # io_bound() execute 100 thread, cost 0.71 second
    multi_thread_tasks(100, io_bound)


def test_multi_thread_io_bound_1000_count():
    # io_bound() execute 1000 thread, cost 18.71 second
    multi_thread_tasks(1000, io_bound)


def test_multi_thread_io_bound_5000_count():
    # io_bound() execute 5000 thread, cost 116.49 second
    multi_thread_tasks(5000, io_bound)


def test_multi_process_cpu_bound():
    # cpu_bound() execute 100 process, cost 26.27 second
    multi_process_tasks(cpu_bound)


def test_multi_process_io_bound():
    # io_bound() execute 100 process, cost 18.24 second
    multi_process_tasks(io_bound)


def test_multi_thread_with_concurrent_cpu_bound_10_thread():
    # 10 thread execute 100 cpu_bound() task with concurrent, cost 60.03 second
    multi_thread_tasks_with_concurrent(10, 100, cpu_bound)


def test_multi_thread_with_concurrent_cpu_bound_20_thread():
    # 20 thread execute 100 cpu_bound() task with concurrent, cost 58.99 second
    multi_thread_tasks_with_concurrent(20, 100, cpu_bound)


def test_multi_thread_with_concurrent_cpu_bound_50_thread():
    # 50 thread execute 100 cpu_bound() task with concurrent, cost 59.56 second
    multi_thread_tasks_with_concurrent(50, 100, cpu_bound)


def test_multi_thread_with_concurrent_cpu_bound_100_thread():
    # 100 thread execute 100 cpu_bound() task with concurrent, cost 59.58 second
    multi_thread_tasks_with_concurrent(100, 100, cpu_bound)


def test_multi_thread_with_concurrent_io_bound_10_thread():
    # 10 thread execute 100 io_bound() task with concurrent, cost 2.24 second
    multi_thread_tasks_with_concurrent(10, 100, io_bound)


def test_multi_thread_with_concurrent_io_bound_20_thread():
    # 20 thread execute 100 io_bound() task with concurrent, cost 3.79 second
    multi_thread_tasks_with_concurrent(20, 100, io_bound)


def test_multi_thread_with_concurrent_io_bound_50_thread():
    # 50 thread execute 100 io_bound() task with concurrent, cost 1.18 second
    multi_thread_tasks_with_concurrent(50, 100, io_bound)


def test_multi_thread_with_concurrent_io_bound_100_thread():
    # 100 thread execute 100 io_bound() task with concurrent, cost 0.66 second
    multi_thread_tasks_with_concurrent(100, 100, io_bound)


def test_multi_process_with_concurrent_cpu_bound_10_process():
    # 10 process execute 100 cpu_bound() task with concurrent, cost 14.78 second
    multi_process_tasks_with_concurrent(10, 100, cpu_bound)


def test_multi_process_with_concurrent_cpu_bound_20_process():
    # 20 process execute 100 cpu_bound() task with concurrent, cost 14.11 second
    multi_process_tasks_with_concurrent(20, 100, cpu_bound)


def test_multi_process_with_concurrent_cpu_bound_50_process():
    # 50 process execute 100 cpu_bound() task with concurrent, cost 17.72 second
    multi_process_tasks_with_concurrent(50, 100, cpu_bound)


def test_multi_process_with_concurrent_cpu_bound_100_process():
    # 报错， windows多进程最大为61
    multi_process_tasks_with_concurrent(100, 100, cpu_bound)


def test_multi_process_with_concurrent_io_bound_10_process():
    # 10 process execute 100 io_bound() task with concurrent, cost 6.43 second
    multi_process_tasks_with_concurrent(10, 100, io_bound)


def test_multi_process_with_concurrent_io_bound_20_process():
    # 20 process execute 100 io_bound() task with concurrent, cost 4.74 second
    multi_process_tasks_with_concurrent(20, 100, io_bound)


def test_multi_process_with_concurrent_io_bound_50_process():
    # 50 process execute 100 io_bound() task with concurrent, cost 9.79 second
    multi_process_tasks_with_concurrent(50, 100, io_bound)


def test_multi_process_with_concurrent_io_bound_100_process():
    # 报错， windows多进程最大为61
    multi_process_tasks_with_concurrent(100, 100, io_bound)


if __name__ == '__main__':
    pytest.main()
