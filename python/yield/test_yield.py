def generator():
    for i in range(10):
        yield i * i


def test_generator():
    g = generator()
    print(g)  # <generator object generator at 0x000001FC672F2F80>
    first = next(g)
    print(f"{first=}")  # first=0
    assert first == 0
    second = next(g)  # second=1
    print(f"{second=}")


def my_generator():
    yield 1
    yield 2
    yield 3


def test_my_generator():
    g = my_generator()
    for val in g:
        print(val)  # 1,2,3


def mygenerater(n):
    for i in range(n):
        print('开始生成...')
        yield i
        print('完成一次...')


def test_mygenerater():
    g = mygenerater(2)
    # 获取生成器中下一个值
    result = next(g)
    print(result) # 开始生成...\n0
    result = next(g)
    print(result) # 完成一次...\n开始生成...\n1

