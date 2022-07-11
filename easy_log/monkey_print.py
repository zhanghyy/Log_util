# -*- coding: utf-8 -*-
# @Time : 2021/9/8 15:17
# @Author :Ben
# @Email :
"""
不直接给print打补丁，自己重新赋值。

"""
import multiprocessing
import os
import sys
import time
import traceback
from easy_log import log_config_default

print_raw = print


def stdout_write(msg: str):
    sys.stdout.write(msg)
    sys.stdout.flush()


def stderr_write(msg: str):
    sys.stderr.write(msg)
    sys.stderr.flush()


# noinspection PyProtectedMember,PyUnusedLocal,PyIncorrectDocstring,DuplicatedCode
def nb_print(*args, sep=' ', end='\n', file=None, flush=True):
    """
    超流弊的print补丁
    :param x:
    :return:
    """
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    if file == sys.stderr:
        stderr_write(sep.join(args))  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
    elif file in [sys.stdout, None]:
        # 获取被调用函数在被调用时所处代码行数
        line = sys._getframe().f_back.f_lineno
        # 获取被调用函数所在模块文件名
        file_name = sys._getframe(1).f_code.co_filename
        #file_name = os.path.basename(file_name)
        # sys.stdout.write(f'"{__file__}:{sys._getframe().f_lineno}"    {x}\n')
        if log_config_default.DEFAULUT_USE_COLOR_HANDLER:
            if log_config_default.DISPLAY_BACKGROUD_COLOR_IN_CONSOLE:
                stdout_write(
                    f'\033[0;34m{time.strftime("%Y-%m-%d %H:%M:%S")}  "{file_name}:{line}"   \033[0;30;44m{sep.join(args)}\033[0m{end} \033[0m')  # 36  93 96 94
            else:
                stdout_write(
                    f'\033[0;34m{time.strftime("%Y-%m-%d %H:%M:%S")}  "{file_name}:{line}"   {sep.join(args)} {end} \033[0m')  # 36  93 96 94
            # sys.stdout.write(f'\033[0;30;44m"{file_name}:{line}"  {time.strftime("%H:%M:%S")}  {"".join(args)}\033[0m\n')
        else:
            stdout_write(
                f'{time.strftime("%Y-%m-%d %H:%M:%S")}  "{file_name}:{line}"   {sep.join(args)} {end}')  # 36  93 96 94
    else:  # 例如traceback模块的print_exception函数 file的入参是   <_io.StringIO object at 0x00000264F2F065E8>，必须把内容重定向到这个对象里面，否则exception日志记录不了错误堆栈。
        print_raw(*args, sep=sep, end=end, file=file)


# noinspection PyPep8,PyUnusedLocal
def print_exception(etype, value, tb, limit=None, file=None, chain=True):
    """
    避免每行有两个可跳转的，导致第二个可跳转的不被ide识别。
    主要是针对print_exception，logging.exception里面会调用这个函数。

    :param etype:
    :param value:
    :param tb:
    :param limit:
    :param file:
    :param chain:
    :return:
    """
    if file is None:
        file = sys.stderr
    for line in traceback.TracebackException(
        type(value), value, tb, limit=limit).format(chain=chain):
        # print(line, file=file, end="")
        if file != sys.stderr:
            stderr_write(f'{line} \n')
        else:
            stdout_write(f'{line} \n')


# print = nb_print

def patch_print():
    """
    Python有几个namespace，分别是

    locals

    globals

    builtin

    其中定义在函数内声明的变量属于locals，而模块内定义的函数属于globals。


    https://codeday.me/bug/20180929/266673.html   python – 为什么__builtins__既是模块又是dict

    :return:
    """
    try:
        __builtins__.print = nb_print
    except AttributeError:
        """
        <class 'AttributeError'>
        'dict' object has no attribute 'print'
        """
        # noinspection PyUnresolvedReferences
        __builtins__['print'] = nb_print
    # traceback.print_exception = print_exception  # file类型为 <_io.StringIO object at 0x00000264F2F065E8> 单独判断，解决了，不要加这个。


def common_print(*args, sep=' ', end='\n', file=None):
    args = (str(arg) for arg in args)
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    if file == sys.stderr:
        stderr_write(sep.join(args) + end)  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
    else:
        stdout_write(sep.join(args) + end)


def reverse_patch_print():
    """
    提供一个反猴子补丁，恢复print原状
    :return:
    """
    # try:
    #     __builtins__.print = common_print
    # except AttributeError:
    #     __builtins__['print'] = common_print

    try:
        __builtins__.print = print_raw
    except AttributeError:
        __builtins__['print'] = print_raw


def is_main_process():
    return multiprocessing.process.current_process().name == 'MainProcess'


# noinspection DuplicatedCode
def only_print_on_main_process(*args, sep=' ', end='\n', file=None, flush=True):
    # 获取被调用函数在被调用时所处代码行数
    if is_main_process():
        args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
        if file == sys.stderr:
            stderr_write(sep.join(args))  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
        elif file in [sys.stdout, None]:
            # 获取被调用函数在被调用时所处代码行数
            line = sys._getframe().f_back.f_lineno
            # 获取被调用函数所在模块文件名
            file_name = sys._getframe(1).f_code.co_filename
            # sys.stdout.write(f'"{__file__}:{sys._getframe().f_lineno}"    {x}\n')
            if log_config_default.DEFAULUT_USE_COLOR_HANDLER:
                if log_config_default.DISPLAY_BACKGROUD_COLOR_IN_CONSOLE:
                    stdout_write(
                        f'\033[0;34m{time.strftime("%Y-%m-%d %H:%M:%S")}  "{file_name}:{line}"   \033[0;30;44m{sep.join(args)}\033[0m{end} \033[0m')  # 36  93 96 94
                else:
                    stdout_write(
                        f'\033[0;34m{time.strftime("%Y-%m-%d %H:%M:%S")}  "{file_name}:{line}"   {sep.join(args)} {end} \033[0m')  # 36  93 96 94
                # sys.stdout.write(f'\033[0;30;44m"{file_name}:{line}"  {time.strftime("%H:%M:%S")}  {"".join(args)}\033[0m\n')
            else:
                stdout_write(
                    f'{time.strftime("%Y-%m-%d %H:%M:%S")}  "{file_name}:{line}"   {sep.join(args)} {end}')  # 36  93 96 94
        else:  # 例如traceback模块的print_exception函数 file的入参是   <_io.StringIO object at 0x00000264F2F065E8>，必须把内容重定向到这个对象里面，否则exception日志记录不了错误堆栈。
            print_raw(*args, sep=sep, end=end, file=file)


if __name__ == '__main__':
    print('before patch')
    patch_print()
    print(0)
    nb_print(123, 'abc')
    print(456, 'def')
    print('http://www.baidu.com')

    reverse_patch_print()
    common_print('hi')

    import logging

    try:
        1 / 0
    except Exception as e:
        logging.exception(e)
