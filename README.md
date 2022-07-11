# ***easy_log***

* “easy_log”简单易用的日志模块

## ***特性***

> 1. 自动转换print效果
>    
>    + 自动转换print效果，再也不怕有人在项目中随意print，导致很难找到是从哪里冒出来的print。
>    + 只要import easy_log，项目所有地方的print自动现型并在控制台可点击几精确跳转到print的地方。
> 2. 兼容性
>    
>    + 使用的是python的内置logging封装的，返回的logger对象的类型是py官方内置日志的Logger类型，兼容性强，
>    + 保证了第三方各种handlers扩展数量多和方便，和一键切换现有项目的日志。
>    
>    * 比如logru和logbook这种三方库，完全重新写的日志，它里面主要被用户使用的logger变量类型不是python内置Logger类型，造成logger说拥有的属性和方法有的不存在或者不一致，这样的日志和python内置的经典日志兼容性差，只能兼容（一键替换logger类型）一些简单的debug info warning errror等方法，。
> 3. 日志命名空间独立
>    
>    + 采用了多实例logger，按日志命名空间区分。
>      命名空间独立意味着每个logger单独的日志界别过滤，单独的控制要记录到哪些地方。
> 4. 对内置looging包打了猴子补丁，使日志永远不会使用同种handler重复记录
>    
>    + 例如，原生的
> 
> ```python
> from logging import getLogger,StreamHandler
> logger = getLogger('hi')
> getLogger('hi').addHandler(StreamHandler())
> getLogger('hi').addHandler(StreamHandler())
> getLogger('hi').addHandler(StreamHandler())
> logger.warning('啦啦啦')
> ```
> 
> + 明明只warning了一次，但实际会造成 啦啦啦 在控制台打印3次。
> + 使用easy_log，对同一命名空间的日志，可以无惧反复添加同类型handler，不会重复记录。
> 
> 5. 支持日志自定义
>    运行此包后，会自动在你的python项目根目录中生成log_config.py文件，按说明修改。

## 项目结构

```
Easy_log
│  example.py    #使用示例
│  README.md     
│  setup.py      
└─easy_log
    │  file_lock.py   #日志文件锁
    │  handlers.py    #日志处理模块
    │  log_config_default.py     #日志默认配置
    │  log_manager.py            #主函数模块
    │  monkey_print.py           #print补丁
    │  set_log_config.py         #用于生成配置文件（附件）
    └─__init__.py
```

## 安装

代码对 Python 3 均兼容

* 半自动安装：先git拉取代码 ，后运行 `python setup.py install`
* 手动安装：将 easy_log 目录放置于当前目录或者 site-packages 目录
* 通过 `import easy_log ` 来引用
  
  <br><br>

## ***用法***

### ***pycahrm颜色设置***

```
要说明的是，即使是同一个颜色代码在pycahrm不同主题都是颜色显示区别很大的，默认的可能很丑或者由于颜色不好导致文字看不清晰
为了达到我这种色彩效果需要重新设置主题颜色，在控制台输出的第一行就教大家怎么设置颜色了。
也可以按下面设置，需要花30秒设置。

"""
1)使用pycharm时候，建议重新自定义设置pycharm的console里面的主题颜色。
设置方式为 打开pycharm的 file -> settings -> Editor -> Color Scheme -> Console Colors 选择monokai，
并重新修改自定义6个颜色，设置Blue为1585FF，Cyan为06B8B8，Green 为 05A53F，Magenta为 ff1cd5,red为FF0207，yellow为FFB009。
如果设置为显示背景色快，由于不同版本的pycahrm或主题，可以根据控制台实际显示设置 White 为 1F1F1F， Black 为 FFFFFF，因为背景色是深色，前景色的文字设置为白色比黑色好。

2)使用xshell或finashell工具连接linux也可以自定义主题颜色，默认使用shell连接工具的颜色也可以。

颜色效果如连接 https://i.niupic.com/images/2020/11/04/8WZf.png

在当前项目根目录的 log_config.py 中可以修改当get_logger方法不传参时后的默认日志行为。

"""
```

### 设置不使用背景色块。

* 在项目根目录下自动生成的log_config.py配置文件中设置

```python
DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = False
```

### 设置既不使用背景色块也不使用彩色文字

* 例如只希望使用easy_log的强大多进程文件切片的功能等其他功能，对彩色控制台日志不感兴趣，则可以设置完全不要彩色。
* 在项目根目录下自动生成的log_config.py配置文件中设置

```python
DEFAULUT_USE_COLOR_HANDLER = False
```

<br>

## Example

#### 1. ***最简单的使用方式,这只是演示控制台日志***

- 自动拦截改变项目中所有地方的print效果。（支持配置文件自定义关闭转化print）
- 控制台日志变成可点击，精确跳转。（支持配置文件自定义修改或增加模板，内置了7种模板，部分模板生成的日志可以在pycharm控制台点击跳转）
- 控制台日志根据日志级别自动变色。（支持配置文件关闭彩色或者关闭背景色块）

```python
from easy_log import LogManager,get_logger

# logger = LogManager('lalala').get_logger_and_add_handlers()
logger = get_logger('lalala') # 这个和上面的效果一样，但上面的LogManager还有其他公有方法可以使用。

logger.debug('绿色')
logger.info('蓝色')
logger.warning('黄色')
logger.error('紫红色')
logger.critical('血红色')
print('print样式被自动发生变化')
```

#### 2. ***easy_log日志文件***

+ easy_log文件日志的自定义filehandler支持多进程下日志文件按大小自动切割。
+ 在各种filehandler实现难度上
  单进程永不切割 <  多进程按时间切割 < 单进程按大小切割  << 多进程按大小切割
  + logging包的RotatingFileHandler多进程运行代码时候，如果要实现向文件写入到规定大小时候并自动备份切割，win和linux都报错。
  + 支持多进程安全切片的知名的handler有ConcurrentRotatingFileHandler，
    此handler能够确保win和linux切割正确不出错，此包在linux使用的是高效的fcntl文件锁，
    在win上性能惨不忍睹。
+ easy_log是基于自动批量聚合，从而减少写入次数（但文件日志的追加最多会有1秒的延迟），从而大幅度减少反复给文件加锁解锁，
  使快速大量写入文件日志的性能大幅提高，在保证多进程安全且排列的前提下，对比这个ConcurrentRotatingFileHandler
  使win的日志文件写入速度提高100倍，在linux上写入速度提高10倍。

```python
logger = get_logger('log', log_filename='aa.log', is_add_stream_handler=False, log_path='./', log_file_size=20,
log_file_handler_type=1)
"""
:param name: 日志命名空间，重要。
:param is_add_stream_handler: 是否打印日志到控制台
:param log_path: 设置存放日志的文件夹路径,如果不设置，则取nb_log_config.LOG_PATH，如果配置中也没指定则自动在代码所在磁盘的根目录创建/pythonlogs文件夹，
非windwos下要注意账号权限问题(如果python没权限在根目录建/pythonlogs，则需要手动先创建好)
:param log_filename: 日志的名字，仅当log_path和log_filename都不为None时候才写入到日志文件。
:param log_file_size :日志大小，单位M，默认100M
:param log_file_handler_type :这个值可以设置为1 2 3 4 四种值，1为使用多进程安全按日志文件大小切割的文件日志，
2为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个日志
3为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题)
4为 WatchedFileHandler，这个是需要在linux下才能使用，需要借助lograte外力进行日志文件的切割，多进程安全。
"""
```

#### 3. ***多实例logger***

- 采用了多实例logger，按日志命名空间区分。
- 命名空间独立意味着每个logger单独的日志界别过滤，单独的控制要记录到哪些地方。>

```python
logger_aa = get_logger('aa')
    logger_bb = get_logger('bb',log_filename='bb.log',is_add_stream_handler=False)
    logger_cc = get_logger('cc',log_level_int=4)        #最低输出等级为error
    logger_dd = get_logger('dd', formatter_template=3)  #使用了不同模板

    logger_aa.info('这是logger_aa的info')
    logger_aa.error('这是logger_aa的error')

    logger_bb.info('这是logger_bb的info,但只输出到文件')
    logger_bb.error('这是logger_bb的error,但只输出到文件')

    logger_cc.info('这是logger_cc的info，但输出级别为error')
    logger_cc.error('这是logger_cc的error')

    logger_dd.info('这是logger_dd的info')
    logger_dd.error('这是logger_dd的error')
```

#### 4. ***捕获第三方python包、库、框架的日志***

- 大部分第三方包的源码的大量文件中都有写   logger = logging.getLogger(__name__)  这段代码。
  假设第三包的包名是  packagex, 这个包下面有 ./dira/dirb/yy.py 文件，假设logger = logging.getLogger(__name__)  这段代码在 ./dira/dirb/moduley.py文件中，当使用这个三方包时候，就会有一个 packagex.dira.dirb.yy.moduley 的命名空间的日志，如果你很在意这个模块的日志，希望吧这个模块的日志捕获出来，那么可以 logger = logging.getLogger("packagex.dira.dirb.moduley"),然后对logger添加文件和控制台等各种handler，设置合适的日志级别，就可以显示出来这个模块的日志了。

```python
"""代码例子如下，因为requests调用了urllib3，这里有urllib3的命名空间的日志，只是没有添加日志handler所以没显示出来。
easy_log.get_logger 自动加上handler和设置日志模板了，方便你调试你所关心的模块的日志。"""
from easy_log import get_logger
import requests

get_logger('urllib3')  # 也可以更精确只捕获 urllib3.connectionpool 的日志，不要urllib3包其他模块文件的日志
requests.get("http://www.baidu.com")
```

#### 5. ***日志优先默认配置***

+ 只要项目任意文件运行了，带有import easy_log的脚本，就会在项目根目录下生成log_config.py配置文件。
+ log_config.py的内容如下，默认都是用#注释了，如果放开某项配置则优先使用这里的配置，否则使用log_config_default.py中的配置。

配置示例如下：

```
如果反对日志有各种彩色，可以设置 DEFAULUT_USE_COLOR_HANDLER = False
如果反对日志有块状背景彩色，可以设置 DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = False
如果想改变日志模板，可以设置 FORMATTER_KIND 参数，只带了9种模板，可以自定义添加喜欢的模板
```

<br/><br/><br/><br/>

---

# 附：

### 演示文件日志，并且直接演示高难度的多进程安全切片文件日志

```python
from multiprocessing import Process
from easy_log import LogManager,get_logger

#指定log_filename不为None 就自动写入文件了，并且默认使用的是多进程安全的切割方式的filehandler。
#默认都添加了控制台日志，如果不想要控制台日志，设置is_add_stream_handler=False
#为了保持方法入场数量少，具体的切割大小和备份文件个数有默认值，
#如果需要修改切割大小和文件数量，在当前python项目根目录自动生成的easy_log_config.py文件中指定。

#logger = LogManager('ha').get_logger_and_add_handlers(is_add_stream_handler=True,
#log_filename='ha.log')
#get_logger这个和上面一句一样。但LogManager不只有get_logger_and_add_handlers一个公有方法。
logger = get_logger(is_add_stream_handler=True,log_filename='ha.log') 

def f():
    for i in range(1000000000):
        logger.debug('测试文件写入性能，在满足 1.多进程运行 2.按大小自动切割备份 3切割备份瞬间不出错'
                    '这3个条件的前提下，验证这是不是python史上文件写入速度遥遥领先 性能最强的python logging handler')
   
if __name__ == '__main__':
    [Process(target=f).start() for _ in range(10)]
```

### 演示文件大小切割在多进程下的错误例子

- 注意说的是多进程，任何handlers在多线程下都没有问题，任何handlers在记录时候都加了线程锁了，完全不用考虑多线程。
  线程锁不能跨进程特别是跨不同批次启动的脚本运行的解释器。
  所以说的是多进程，不是多线程。
- 下面这段代码会疯狂报错。因为每达到100kb就想切割，多个文件句柄引用了同一个文件，某个进程想备份改文件名，别的进程不知情。
- 解决这种问题，有人会说用进程锁，那是不行的，如果把xx.py分别启动两次，没有共同的父子进程，属于跨解释器的，进程锁是不行的。
- easy_log是采用的文件锁，文件锁在linux性能比较好，在win很差劲，导致日志拖累真个代码的性能，所以easy_log是采用把每1秒内的日志聚合起来，写入一次文件，从而大幅减少了加锁解锁次数，
  对比有名的concurrent_log_handler包的ConcurrentRotatingFileHandler，在win上疯狂快速写日志的性能提高了100倍，在linux上也提高了10倍左右的性能。

```python
"""
只要满足3个条件
1.文件日志
2.文件日志按大小或者时间切割
3.多进程写入同一个log文件，可以是代码内部multiprocess.Process启动测试，
  也可以代码内容本身不用多进程但把脚本反复启动运行多个来测试。

把切割大小或者切割时间设置的足够小就很容易频繁必现，平时有的人没发现是由于把日志设置成了1000M切割或者1天切割，
自测时候只随便运行一两下就停了，日志没达到需要切割的临界值，所以不方便观察到切割日志文件的报错。

这里说的是多进程文件日志切割报错即多进程不安全，有的人强奸民意转移话题老说他多线程写日志切割日志很安全，简直是服了。
面试时候把多进程和多线程区别死记硬背 背的一套一套很溜的，结果实际运用连进程和线程都不分。
"""
from logging.handlers import  RotatingFileHandler
import logging
from multiprocessing import Process
from threading import Thread

logger = logging.getLogger('test_raotating_filehandler')

logger.addHandler(RotatingFileHandler(filename='testratationg.log',maxBytes=1000 *100,backupCount=10))

def f():
    while 1:
        logger.warning('这个代码会疯狂报错，因为设置了100Kb就切割并且在多进程下写入同一个日志文件'*20)

if __name__ == '__main__':
    for _ in range(10):
        Process(target=f).start()  # 反复强调的是 文件日志切割并且多进程写入同一个文件，会疯狂报错
        # Thread(target=f).start()  # 多线程没事，所有日志handler无需考虑多线程是否安全，说的是多进程文件日志切割不安全，你老说多线程干嘛？
```

### 使用火热的loguru 来演示惨烈的文件日志重复记录。

```python
"""
这也是一个很惨烈的真实例子。使用大火的 loguru ，然来用户让来本意是想实现每天生成一个新的日志文件。
结果造成了在所有历史文件中都重复记录当前日志，随着部署的天数越来越长，长时间例如半年 八九个月 如果不重新部署程序，
会造成严重的磁盘紧张和cpu飙升。
"""

from  loguru import logger
import time


def f(x):
    """
     用户实际生产是想每一天生成一个日志， time.strftime("%Y-%m-%d")}.log，
     但这里为了节约时间方便演示文件日志重复记录所以换成时分秒演示，不然的话要观察很长的时间每隔一天观察一次才能观察出来。
    """
    logger.add(f'test_{time.strftime("%H-%M-%S")}.log')
    logger.debug(f'loguru 太惨了重复记录 {x}')
    logger.info(f'loguru 太惨了重复记录 {x}')
    logger.warning(f'loguru 太惨了重复记录 {x}')
    logger.error(f'loguru 太惨了重复记录 {x}')
    logger.critical(f'loguru 太惨了重复记录 {x}')

for i in range(100):
    time.sleep(1)
    f(i)

"""
预期是每秒调用一次函数f，但函数里面面有5次记录，debug info warning error  critical，
所以预期是每秒有5条日志只写入当前最新的日志文件中，但结果是每秒都写入到历史所有日志文件中。
只看当前最新的那个日志文件，似乎没有看到重复记录，但如果看所有的历史旧日志文件可以看到每个旧文件都严重重复记录了。
这种问题很难排查，所以用日志要谨慎，要搞懂日志handlers，和设计模式的观察者模式才能用好日志。
"""
```

## easy_log对比 loguru

### 1. 控制台屏幕流日志颜色。

+ 1.1 easy_log 颜色更炫
+ 1.2 easy_log 自动使用猴子补丁全局改变任意print
+ 1.3 easy_log 支持控制台点击日志文件行号自动打开并跳转到精确的文件和行号。

### 2. 文件日志性能，easy_log比loguru快400%。

```
easy_log为了保证多进程下按大小安全切割，采用了文件锁 + 自动每隔1秒批量把消息写入到文件，大幅减少了加锁解锁和判断时候需要切割的次数。
easy_log的file_handler是史上最强的，超过了任何即使不切割文件的内置filehandler,比那些为了维护自动切割的filehandler例如logging内置的
RotatingFileHandler和TimedRotatingFileHandler的更快。比为了保证多进程下的文件日志切割安全的filehandler更是快多了。

比如以下star最多的，为了确保多进程下切割日志文件的filehandler  
https://github.com/wandaoe/concurrent_log
https://github.com/unlessbamboo/ConcurrentTimeRotatingFileHandler
https://github.com/Preston-Landers/concurrent-log-handler

easy_log的多进程文件日志不仅是解决了文件切割不出错，而且写入性能远超这些4到100倍。
100倍的情况是 win10 + https://github.com/Preston-Landers/concurrent-log-handler对比easy_log
easy_log的文件日志写入性能是loguru的4倍，但loguru在多进程运行下切割出错。
```

##### loguru快速文件写入性能，写入200万条代码

这个代码如果rotation设置10000 Kb就切割，那么达到切割会疯狂报错，为了不报错测试性能只能设置为1000000 KB

```python
import time

from  loguru import logger
from concurrent.futures import ProcessPoolExecutor


logger.remove(handler_id=None)

logger.add("./log_files/loguru-test1.log",enqueue=True,rotation="10000 KB")

def f():
    for i in range(200000):
        logger.debug("测试多进程日志切割")
        logger.info("测试多进程日志切割")
        logger.warning("测试多进程日志切割")
        logger.error("测试多进程日志切割")
        logger.critical("测试多进程日志切割")


pool = ProcessPoolExecutor(10)
if __name__ == '__main__':
    """
    100万条需要115秒
    15:12:23
    15:14:18
  
    200万条需要186秒
    """
    print(time.strftime("%H:%M:%S"))
    for _ in range(10):
        pool.submit(f)
    pool.shutdown()
    print(time.strftime("%H:%M:%S"))
```

###### easy_log快速文件写入性能，写入200万条代码

```python
from easy_log import get_logger
from concurrent.futures import ProcessPoolExecutor
logger = get_logger('test_easy_log_conccreent',is_add_stream_handler=False,log_filename='test_easy_log_conccreent.log')


def f(x):
    for i in range(200000):
        logger.warning(f'{x} {i}')

if __name__ == '__main__':
    # 200万条 45秒
    pool = ProcessPoolExecutor(10)
    print('开始')
    for i in range(10):
        pool.submit(f,i)
    pool.shutdown()
    print('结束')
```

### 3. 多进程下的文件日志切割，easy_log不出错，loguru出错导致丢失大量日志。

```
将10.2的代码运行就可以发现，loguru设置了10M大小切割，疯狂报错，因为日志在达到指定大小后切割需要备份重命名，
造成其他的进程出错。

win10 + python3.6 + loguru 0.5.3(任何loguru版本都报错，已设置enqueue=True)
出错如下。
Traceback (most recent call last):
  File "F:\minicondadir\Miniconda2\envs\py36\lib\site-packages\loguru\_handler.py", line 287, in _queued_writer
    self._sink.write(message)
  File "F:\minicondadir\Miniconda2\envs\py36\lib\site-packages\loguru\_file_sink.py", line 174, in write
    self._terminate_file(is_rotating=True)
  File "F:\minicondadir\Miniconda2\envs\py36\lib\site-packages\loguru\_file_sink.py", line 205, in _terminate_file
    os.rename(old_path, renamed_path)
PermissionError: [WinError 32] 另一个程序正在使用此文件，进程无法访问。: 'F:\\coding2\\easy_log\\tests\\log_files\\loguru-test1.log' -> 'F:\\coding2\\easy_log\\tests\\log_files\\loguru-test1.2021-08-25_15-12-23_434270.log'
--- End of logging error ---
```

```
python性能要发挥好，必须开多进程。
例如django flask的部署用gunicorn uwsgi都是自动开多进程+线程(协程)，即使你的代码里面没亲自写多进程运行，但是自动被迫用了多进程。
即使你代码没亲自写多进程，例如在同一个机器反复把xx.py启动部署10次，相当于10个进程的日志都写到 yyyy.log,一样是被迫相当于10个进程了。
所以多进程文件日志切割安全很重要。

有的人说自己多进程写文件日志没出错，那是你没设置成按大小或者时间切割，或者自己设置了1G大小切割或者按天切割，不容易观察到。
只要你把时间设置成每1分钟切割或者10M切割，就会很快很容易观察到了。
如果文件日志不进行切割，多进程写同一个文件不会出错的。
```

### 4. 写入不同的文件，easy_log采用经典日志的命名空间区分日志，比loguru更简单

```python
from easy_log import get_logger
from loguru import logger

# easy_log 写入不同的文件是根据日志命名空间 name 来区分的。方便。
logger_a = get_logger('a',log_filename='a.log',log_path='./log_files')
logger_b = get_logger('b',log_filename='b.log',log_path='./log_files')
logger_a.info("嘻嘻a")
logger_b.info("嘻嘻b")

# loguru 不同功能为了写入不同的文件，需要设置消息前缀标志。不方便。
logger.add('./log_files/c.log', filter=lambda x: '[特殊标志c!]' in x['message'])
logger.add('./log_files/d.log', filter=lambda x: '[特殊标志d!]' in x['message'])
logger.add('./log_files/e.log', )
logger.info('[特殊标志c!] 嘻嘻c') # 出现在c.log和 e.log  消息为了写入不同文件需要带消息标志
logger.info('[特殊标志d!] 嘻嘻d') # 出现在d.log和 e.log  消息为了写入不同文件需要带消息标志
```

### 5. 按不同功模块能作用的日志设置不同的日志级别。loguru无法做到。

##### 例如a模块的功能希望控制台日志可以显示debug，b模块的功能只显示info以上级别。

```python
import logging
from easy_log import get_logger

# easy_log 写入不同的文件是根据日志命名空间 name 来区分的。方便。
logger_a = get_logger('a',log_level_int=logging.DEBUG)
logger_b = get_logger('b',log_level_int=logging.INFO)
logger_a.debug("嘻嘻a debug会显示")
logger_a.info("嘻嘻a info会显示")
logger_b.debug("嘻嘻b debug不会显示")
logger_b.info("嘻嘻b info会显示")
```

### 6. 比第三方的日志handler扩展数量，easy_log完胜loguru

```
日志能记载到什么地方是由handler决定的，很多人以为日志等于控制台 + 文件，并不是这样的。
日志可以记载到任何介质，不是只有控制台和文件。
easy_log的核心方法是get_logger，此方法是返回原生loggin.Logger类型的对象，
原生日志可扩展的第三方handler包在pypi官网高达几百个，可以直接被easy_log使用。
```

### 7. easy_log的get_logger返回类型是原生经典logging.Logger，兼容性达到了100%。loguru独立实现日志系统，兼容性很差。

```
绝大部分python代码采用的是内置经典的python logging模块，
例如老代码 
logger = logging.getLogger("my_namespage")

老代码的其他地方使用了logger对象的这些方法，远不止这两个。
logger.setLevel()
logger.addHandler()

如果是改成easy_log,  logger = easy_log.get_logger("my_namespage")
那么logger.setLevel() logger.addHandler() 仍然可以正常使用。

如果是改成loguru， from loguru import logger
那么logger.setLevel() logger.addHandler() 会是代码报错，因为loguru的logger对象是独立特行独自实现的类型，没有这些方法。
```

### 8. 易用性对比，easy_log的控制台和文件handler比loguru添加更容易

```
loguru哪里好了？
loguru只是自动有好看的日志formatter显示格式 + 比原生logger更容易添加文件handler。
loguru比原生logging也只是好在这两点而已，其他方面这不如原生。

easy_log 比loguru添加控制台和文件日志更简单，并且显示格式更炫。loguru对比原生logging的两个优势在easy_log面前没有了。
```

### 9. easy_log可以灵活捕获所有第三方python包、库、框架的日志,loguru不行

