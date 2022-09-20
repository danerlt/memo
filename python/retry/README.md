# retry

Python中retry库整理

## tenacity

[tenacity](https://github.com/jd/tenacity) 库是在 Apscheduler 4.0的代码里面发现的这个库.
这个库是从 [retrying](https://github.com/rholder/retrying) fork 出来的, retrying 库从2016年开始就没有维护.

截止2022年9月20日,这个库的 stars 有4.1k ,用的人数还比较多,功能比较强大.重试需求复杂的场景推荐使用.

### 安装

```shell
pip install tenacity
```

### 示例

文档地址见: [https://tenacity.readthedocs.io/en/latest/](https://tenacity.readthedocs.io/en/latest/)

下面是一些常用的示例:

```python
#!/usr/bin/env python  
# -*- coding:utf-8 -*-
import datetime

from tenacity import retry, wait_fixed, stop_after_attempt, stop_after_delay, retry_if_exception_type, wait_random,
    wait_exponential


def get_now():
    fmt = "%Y-%m-%d %H:%M:%S"
    now = datetime.datetime.now().strftime(fmt)
    return now


def foo():
    now = get_now()
    print(f"等待重试...: now: {now}")
    a = 1
    b = 0
    print(f"a: {a}, b:{b}")
    res = a / b
    return res


@retry
def t_retry():
    foo()


@retry(wait=wait_fixed(2))
def t_retry_awit():
    """等待两秒,一直重试,直到运行成功"""
    foo()


@retry(wait=wait_random(min=1, max=2))
def t_retry_wait_random_1_to_2_s():
    """一直重试,每次重试等待1到2秒"""
    foo()


@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def t_retry_wait_exponential_1():
    """一直重试,每次重试等待2 ^ x * multiplier 秒, 最小4秒,最大10秒, 指数默认为2
    关键词: 指数退避
    """
    foo()


@retry(wait=wait_fixed(3) + wait_random(0, 2))
def t_retry_wait_fixed_jitter():
    """等待 3秒+0到2秒随机延迟"""
    foo()


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def t_retry_wait_count():
    """等待重试3次,每次重试等待2秒"""
    foo()


@retry(stop=stop_after_delay(10), wait=wait_fixed(2))
def t_retry_wait_time():
    """重试10秒后不在重试, 每次重试等待2秒"""
    foo()


@retry(stop=(stop_after_delay(10) | stop_after_attempt(7)), wait=wait_fixed(2))
def t_retry_wait_time_or_count():
    """重试10秒后或者重试7次不在重试, 每次重试等待2秒"""
    foo()


@retry(retry=retry_if_exception_type(ZeroDivisionError), wait=wait_fixed(2))
def t_retry_in_exception():
    """如果抛了ZeroDivisoinError就重试,每次重试等待2秒"""
    foo()


@retry(retry=retry_if_exception_type(ZeroDivisionError), stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
def t_retry_raise_origin_exception():
    """如果抛了ZeroDivisoinError就重试,重试3次,每次重试等待2秒,如果最终还是失败抛出原来的异常"""
    foo()


def error_callback(retry_state):
    """retry失败的回调函数,必须要传retry_state参数"""
    print("失败执行回调函数")
    exception = retry_state.outcome.exception
    print(f"exception: {exception}")


@retry(retry_error_callback=error_callback, stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
def t_retry_error_callback():
    """重试最终失败调用回调函数,重试3次,每次重试等待2秒,如果最终还是失败抛出原来的异常"""
    foo()


if __name__ == '__main__':
    # t_retry()
    # t_retry_awit()
    # t_retry_wait_random_1_to_2_s()
    # t_retry_wait_exponential_1()
    # t_retry_wait_fixed_jitter()
    # t_retry_wait_count()
    # t_retry_wait_time()
    # t_retry_wait_time_or_count()
    # t_retry_in_exception()
    # t_retry_raise_origin_exception()
    t_retry_error_callback()


```

### 源码记录

目录结构

```
├── after.py
├── before.py
├── before_sleep.py
├── nap.py
├── py.typed
├── retry.py
├── stop.py
├── tornadoweb.py
├── wait.py
├── _asyncio.py
├── _utils.py
├── __init__.py  retry装饰器的定义
```

在我们使用的retry的时候会调用tenacity/__init__.py中的retry方法,如下,这个方法返回一个函数. 

如果使用的是@retry或者@retry(),直接返回retry()(dargs[0]),否则就返回一个装饰器函数,这个函数里面会判断被装饰的函数的类型.

如果是协程,就生成AsyncRetrying对象,如果是tornado相关就生成TornadoRetrying对象,否则就生成Retrying对象,一般情况就会生成这个类的对象.

```python
def retry(*dargs: t.Any, **dkw: t.Any) -> t.Union[WrappedFn, t.Callable[[WrappedFn], WrappedFn]]:  # noqa
    """Wrap a function with a new `Retrying` object.

    :param dargs: positional arguments passed to Retrying object
    :param dkw: keyword arguments passed to the Retrying object
    """
    # support both @retry and @retry() as valid syntax
    if len(dargs) == 1 and callable(dargs[0]):
        return retry()(dargs[0])
    else:

        def wrap(f: WrappedFn) -> WrappedFn:
            if isinstance(f, retry_base):
                warnings.warn(
                    f"Got retry_base instance ({f.__class__.__name__}) as callable argument, "
                    f"this will probably hang indefinitely (did you mean retry={f.__class__.__name__}(...)?)"
                )
            if iscoroutinefunction(f):
                r: "BaseRetrying" = AsyncRetrying(*dargs, **dkw)
            elif tornado and hasattr(tornado.gen, "is_coroutine_function") and tornado.gen.is_coroutine_function(f):
                r = TornadoRetrying(*dargs, **dkw)
            else:
                r = Retrying(*dargs, **dkw)

            return r.wraps(f)

        return wrap

```

Retrying类源码如下,他继承了`BaseRetrying`类,然后实现了`__call__`方法:
```python
class Retrying(BaseRetrying):
    """Retrying controller."""

    def __call__(self, fn: t.Callable[..., _RetValT], *args: t.Any, **kwargs: t.Any) -> _RetValT:
        self.begin()

        retry_state = RetryCallState(retry_object=self, fn=fn, args=args, kwargs=kwargs)
        while True:
            do = self.iter(retry_state=retry_state)
            if isinstance(do, DoAttempt):
                try:
                    result = fn(*args, **kwargs)
                except BaseException:  # noqa: B902
                    retry_state.set_exception(sys.exc_info())
                else:
                    retry_state.set_result(result)
            elif isinstance(do, DoSleep):
                retry_state.prepare_for_next_attempt()
                self.sleep(do)
            else:
                return do
```
`r = Retrying(*dargs, **dkw)`生成Retrying对象的示例的时候会先调用`BaseRetrying`的`__init__`方法.
```python
class BaseRetrying(ABC):
    def __init__(
        self,
        sleep: t.Callable[[t.Union[int, float]], None] = sleep, 
        stop: "stop_base" = stop_never,
        wait: "wait_base" = wait_none(),
        retry: retry_base = retry_if_exception_type(),
        before: t.Callable[["RetryCallState"], None] = before_nothing,
        after: t.Callable[["RetryCallState"], None] = after_nothing,
        before_sleep: t.Optional[t.Callable[["RetryCallState"], None]] = None,
        reraise: bool = False,
        retry_error_cls: t.Type[RetryError] = RetryError,
        retry_error_callback: t.Optional[t.Callable[["RetryCallState"], t.Any]] = None,
    ):
        self.sleep = sleep
        self.stop = stop
        self.wait = wait
        self.retry = retry
        self.before = before
        self.after = after
        self.before_sleep = before_sleep
        self.reraise = reraise
        self._local = threading.local()
        self.retry_error_cls = retry_error_cls
        self.retry_error_callback = retry_error_callback
```

这里会将初始化一些属性.
- sleep 暂停函数,默认是tenacity/nap.py中的sleep方法,调用time.sleep暂停
- stop stop_base类的对象,默认是tenacity/stop.py中的_stop_never类的对象,表示永不停止
- wait wait_base类的对象,默认是tenacity/wait.py中的wait_none类的对象,表示不等待
- retry retry_base类的对象,默认是tenacity/retry.py中的retry_if_exception_type类的对象, 默认异常是Exception和BaseException
- before before函数,默认是tenacity/before.py中的before_nothing函数,函数体为空
- after after函数,默认是tenacity/after.py中的after_nothing函数,函数体为空
- before_sleep 在执行sleep之前执行的函数,默认为None,表示执行sleep之前不用执行对应的函数
- reraise 是否抛出原始异常,默认为False,表示不抛出原始异常,会抛出RetryError
- retry_error_cls retry异常抛出的异常类,默认为tenacity/__init__.py中的RetryError类
- retry_error_callback  retry异常执行的回调函数,默认为None
 
然后调用`Retrying`类的`__call__`方法,
```python
    def __call__(self, fn: t.Callable[..., _RetValT], *args: t.Any, **kwargs: t.Any) -> _RetValT:
        # 初始化statistics字典的数据
        self.begin()
        
        # 然后生成RetryCallState类的对象
        retry_state = RetryCallState(retry_object=self, fn=fn, args=args, kwargs=kwargs)
        while True:
            # 调用iter方法 如果do是DoAttempt对象就执行函数, 如果函数成功就set_result,如果函数抛异常了就执行set_exception
            # 如果do是DoSleep对象就执行sleep方法
            do = self.iter(retry_state=retry_state)
            if isinstance(do, DoAttempt):
                try:
                    result = fn(*args, **kwargs)
                except BaseException:  # noqa: B902
                    retry_state.set_exception(sys.exc_info())
                else:
                    retry_state.set_result(result)
            elif isinstance(do, DoSleep):
                retry_state.prepare_for_next_attempt()
                self.sleep(do)
            else:
                return do
```

先调用RetryCallState类的__init__方法:
```python
class RetryCallState:
    """State related to a single call wrapped with Retrying."""

    def __init__(
        self,
        retry_object: BaseRetrying, 
        fn: t.Optional[WrappedFn], 
        args: t.Any,  
        kwargs: t.Any,
    ) -> None:
        #: 开始时间
        self.start_time = time.monotonic()
        #: BaseRetrying对象
        self.retry_object = retry_object
        #: 被retry装饰的函数
        self.fn = fn
        #: 被retry装饰的函数位置参数
        self.args = args
        #:  被retry装饰的函数关键字参数
        self.kwargs = kwargs

        #: 当前重试的次数,int类型,默认为1
        self.attempt_number: int = 1
        #: 函数产生的最后结果（结果或异常
        self.outcome: t.Optional[Future] = None
        #: 最后结果的时间戳
        self.outcome_timestamp: t.Optional[float] = None
        #: 重试中花费的睡眠时间
        self.idle_for: float = 0.0
        #: 重试管理器决定的下一步操作 RetryAction 对象,默认为None
        self.next_action: t.Optional[RetryAction] = None
```

iter方法
```python
    def iter(self, retry_state: "RetryCallState") -> t.Union[DoAttempt, DoSleep, t.Any]:  # noqa
        # 先从state对象中获取最后结果 
        fut = retry_state.outcome
        if fut is None:
            # 返回结果为None
            if self.before is not None:
                # before函数不为None,执行before函数
                self.before(retry_state)
            # 返回DoAttempt对象
            return DoAttempt()
        
        # 重试
        is_explicit_retry = retry_state.outcome.failed and isinstance(retry_state.outcome.exception(), TryAgain)
        if not (is_explicit_retry or self.retry(retry_state=retry_state)):
            return fut.result()
        
        # 如果after函数不为None执行after函数
        if self.after is not None:
            self.after(retry_state)

        self.statistics["delay_since_first_attempt"] = retry_state.seconds_since_start
        # 执行stop函数
        if self.stop(retry_state=retry_state):
            if self.retry_error_callback:
                # 如果retry_error_callback有值 调用回调函数
                return self.retry_error_callback(retry_state)
            # 异常处理
            retry_exc = self.retry_error_cls(fut)
            if self.reraise:
                # 如果reraise为True 抛出 retry_exc.reraise()
                raise retry_exc.reraise()
            # reraise为False 从fut.exception()抛异常
            raise retry_exc from fut.exception()
        
        if self.wait:
            # 如果wait有值 执行wait对象的__call__方法 sleep表等待的秒数
            sleep = self.wait(retry_state=retry_state)
        else:
            sleep = 0.0
        # 修改state对象
        retry_state.next_action = RetryAction(sleep)
        retry_state.idle_for += sleep
        self.statistics["idle_for"] += sleep
        self.statistics["attempt_number"] += 1

        if self.before_sleep is not None:
            # 如果before_sleep方法不为None,执行before_sleep方法
            self.before_sleep(retry_state)
        
        # 返回DoSleep对象
        return DoSleep(sleep)
```

## retry

[retry](https://github.com/invl/retry) 库,截止2022年9月20日,这个库的 stars 有0.5k ,用的人数还比较少.

且从2016年之后也没有维护了.但用法比较简单,重试不复杂的情况下可以使用.

### 安装

```
pip install retry
```

### 装饰器

```python
def retry(exceptions=Exception, tries=-1, delay=0, max_delay=None, backoff=1, jitter=0, logger=logging_logger):
    """Return a retry decorator.

    :param exceptions: 要捕获的异常或异常元组。默认值：Exception
    :param tries: 最大重试次数。默认值：-1（无限）。
    :param delay: 重试之间的初始延迟。默认值：0。
    :param max_delay: 延迟的最大值。默认值：None（无限制）
    :param backoff: 重试延迟的倍数. 默认值: 1 (1倍).
    :param jitter: 重新之间的延迟增加了额外的秒数。默认值：0. 如果是数字，则为固定，如果为元组，则为随机（最小，最大）
    :param logger: logger.warning(fmt, error, delay) 将在重试失败时调用。默认值：retry.logging_logger。如果为 None，则禁用日志记录。
    """
    _tries, _delay = tries, delay
    while _tries:
        try:
            return f()
        except exceptions as e:
            _tries -= 1
            if not _tries:
                raise

            if logger is not None:
                logger.warning('%s, retrying in %s seconds...', e, _delay)

            time.sleep(_delay)
            _delay *= backoff

            if isinstance(jitter, tuple):
                _delay += random.uniform(*jitter)
            else:
                _delay += jitter

            if max_delay is not None:
                _delay = min(_delay, max_delay)    
```

### 用法

```python
from retry import retry


@retry(ZeroDivisionError, tries=3, delay=1, max_delay=5, backoff=2, jitter=(0, 3))
def bar():
    """如果抛了ZeroDivisionError, 重试3次,每次延迟2秒,最大延迟5秒,每次异常,延迟时间乘以2,每次延迟加上0到3中间的随机秒

    如果还是抛错,将异常抛出"""

    res = 2 / 0
    return res


if __name__ == '__main__':
    import logging

    logging.basicConfig()
    bar()

```
