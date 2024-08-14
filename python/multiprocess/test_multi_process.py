from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from multiprocessing import Process
from threading import Thread
from time import perf_counter


def fib(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def test_fib():
    n = 35
    start = perf_counter()
    res = fib(n)
    print(res)
    end = perf_counter()
    cost = round(end - start, 2)
    # fib(35) cost 5.47 second
    print(f"fib({n}) cost {cost} second")


def test_for_fib():
    n = 35
    for_loop = 5
    res = []
    start = perf_counter()
    for _ in range(for_loop):
        res.append(fib(n))
    end = perf_counter()
    cost = round(end - start, 2)
    print(res)
    # for loop 5 count, fib(35) cost 26.3 second
    print(f"for loop {for_loop} count, fib({n}) cost {cost} second")


def test_multi_thread():
    # 多线程方式 这个默认没有返回值
    n = 35
    thread_num = 5
    start = perf_counter()
    threads = []
    for _ in range(thread_num):
        thread = Thread(target=fib, args=(n,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    end = perf_counter()
    cost = round(end - start, 2)
    # 5 thread count, fib(35) cost 28.17 second
    print(f"{thread_num} thread count, fib({n}) cost {cost} second")


def test_multi_process():
    # 多进程方式，这个默认没有返回值
    n = 35
    process_num = 5
    start = perf_counter()
    process_list = []
    for _ in range(process_num):
        process = Process(target=fib, args=(n,))
        process_list.append(process)
        process.start()

    for process in process_list:
        process.join()
    end = perf_counter()
    cost = round(end - start, 2)
    # 5 process count, fib(35) cost 9.97 second
    print(f"{process_num} process count, fib({n}) cost {cost} second")


def test_multi_thread_with_concurrent():
    n = 35
    thread_num = 5
    start = perf_counter()
    res = []
    with ThreadPoolExecutor(max_workers=thread_num) as executor:
        tasks = []
        for _ in range(thread_num):  # 模拟多个任务
            future = executor.submit(fib, n)
            tasks.append(future)

        for future in as_completed(tasks):  # 并发执行
            res.append(future.result())
    print(res)
    end = perf_counter()
    cost = round(end - start, 2)
    # 5 thread with concurrent, fib(35) cost 28.24 second
    print(f"{thread_num} thread with concurrent, fib({n}) cost {cost} second")
    # 这种方式跟直接使用多线程方式效果一样，但是使用concurrent可以获取返回值


def test_multi_process_with_concurrent():
    n = 35
    process_num = 5
    start = perf_counter()
    res = []
    with ProcessPoolExecutor(max_workers=process_num) as executor:
        tasks = []
        for _ in range(process_num):  # 模拟多个任务
            future = executor.submit(fib, n)
            tasks.append(future)

        for future in as_completed(tasks):  # 并发执行
            res.append(future.result())
    print(res)
    end = perf_counter()
    cost = round(end - start, 2)
    # 5 process with concurrent, fib(35) cost 9.26 second
    print(f"{process_num} process with concurrent, fib({n}) cost {cost} second")
    # 这种方式跟直接使用多进程方式效果一样，但是使用concurrent可以获取返回值
