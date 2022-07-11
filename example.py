# -*- coding: utf-8 -*-
# @Time : 2021/9/8 15:17
# @Author :Ben
# @Email :
from easy_log import get_logger




#简单使用
def example_1():
    '''easy_log简单使用'''
    logger = get_logger('log')
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
    print('print样式被自动发生变化')


# 文件处理
def example_2():
    '''easy_log日志文件,不输出到控制台，is_add_stream_handler=False'''
    logger = get_logger('log', log_filename='aa.log', is_add_stream_handler=False, log_path='./', log_file_size=20,
                        log_file_handler_type=1)
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
    print('日志不输出到控制台！')


# 多实例logger
def example_3():
    '''easy_log多实例log'''
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




# 第三方捕获
def example_4():
    '''捕获所有第三方python包、库、框架的日志'''
    import requests
    get_logger('urllib3')  # 也可以更精确只捕获 urllib3.connectionpool 的日志，不要urllib3包其他模块文件的日志
    requests.get("http://www.baidu.com")



if __name__ == '__main__':
    # 简单使用
    example_1()

    # easy_log的文件处理
    # example_2()

    # easy_log的多实例logger
    # example_3()

    # 捕获第三方包
    # example_4()

    pass








