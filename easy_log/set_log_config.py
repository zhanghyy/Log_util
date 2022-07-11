# -*- coding: utf-8 -*-
# @Time : 2021/9/8 15:17
# @Author :Ben
# @Email :
"""

使用覆盖的方式，做配置。
"""
import sys
import time
import importlib
from pathlib import Path
from easy_log import log_config_default
from easy_log.monkey_print import stdout_write, stderr_write, is_main_process
from shutil import copyfile



def nb_print(*args, sep=' ', end='\n', file=None):
    """
    print补丁
    :param x:
    :return:
    """
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    if file == sys.stderr:
        stderr_write(sep.join(args))  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
    else:
        # 获取被调用函数在被调用时所处代码行数
        line = sys._getframe().f_back.f_lineno
        # 获取被调用函数所在模块文件名
        file_name = sys._getframe(1).f_code.co_filename
        if log_config_default.DISPLAY_BACKGROUD_COLOR_IN_CONSOLE:
            stdout_write(
                f'\033[0;34m{time.strftime("%Y-%m-%d %H:%M:%S")}  "{file_name}:{line}"   \033[0;30;44m{sep.join(args)}\033[0m{end} \033[0m')  # 36  93 96 94
        else:
            stdout_write(
                f'\033[0;34m{time.strftime("%Y-%m-%d %H:%M:%S")}  "{file_name}:{line}"   {sep.join(args)} {end} \033[0m')  # 36  93 96 94


def show_nb_log_config():
    nb_print('显示nb_log 包的默认的低优先级的配置参数')
    for var_name in dir(log_config_default):
        nb_print(var_name, getattr(log_config_default, ':', var_name))
    print('\n')


def use_config_form_log_config_module():
    """
    自动读取配置。会优先读取启动脚本的目录的log_config.py文件。没有则读取项目根目录下的log_config_default.py
    :return:
    """
    line = sys._getframe().f_back.f_lineno
    file_name = sys._getframe(1).f_code.co_filename
    try:
        m = importlib.import_module('log_config')
        msg = f'\n检测到 "{m.__file__}:1" 文件里面的变量作为优先配置了\n'
        if is_main_process():
            pass
            # 如果熟悉配置文件所在目录，注释下面一行，不输出到日志中
            stdout_write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}  "{file_name}:{line}"{msg}\n')
        for var_namex, var_valuex in m.__dict__.items():
            if var_namex.isupper():
                setattr(log_config_default, var_namex, var_valuex)
    except ModuleNotFoundError:
        auto_creat_config_file_to_project_root_path()
        msg = f'''在你的项目根目录下生成了 \n "{Path(sys.path[1]) / Path('log_config.py')}" 的nb_log包的日志配置文件，快去看看并修改一些自定义配置吧'''
        stdout_write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}  "{file_name}:{line}"   {msg} \n \033[0m')


def auto_creat_config_file_to_project_root_path():
    """
    :return:
    """
    if Path(sys.path[1]).as_posix() in Path(__file__).parent.parent.absolute().as_posix():
        pass
        #nb_print('不希望在本项目里面创建')
        #return
    """
            如果没设置PYTHONPATH，sys.path会这样，取第一个就会报错
            ['', '/data/miniconda3dir/inner/envs/mtfy/lib/python36.zip', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/lib-dynload', '/root/.local/lib/python3.6/site-packages', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/site-packages']

            ['', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\python36.zip', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\DLLs', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\multiprocessing_log_manager-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pyinstaller-3.4-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pywin32_ctypes-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\altgraph-0.16.1-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\macholib-1.11-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pefile-2019.4.18-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\Pythonwin']
            """
    if '/lib/python' in sys.path[1] or r'\lib\python' in sys.path[1] or '.zip' in sys.path[1]:
        raise EnvironmentError('''如果用pycahrm启动，默认不需要你手动亲自设置PYTHONPATH，如果你是cmd或者shell中直接敲击python xx.py 来运行，
                                   报现在这个错误，你现在肯定是没有设置PYTHONPATH环境变量，不要设置永久环境变量，设置临时会话环境变量就行，
                                   windows设置  set PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令    
                                   linux设置    export PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令    
                                   ''')
    copyfile(Path(__file__).parent / Path('log_config_default.py'), Path(sys.path[1]) / Path('log_config.py'))


use_config_form_log_config_module()
