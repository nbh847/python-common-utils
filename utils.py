from math import ceil


def page_generator(count: int, page_size: int, start: int = 1) -> [int]:
    """
    页码生成器：根据总数据项和页码大小生成页码编号
    :param count: 总数据项数量
    :param page_size:每页显示的数据项数量
    :param start:（默认值为1）页面编号的起始值
    :return:
    """
    for page in range(start, int(ceil(count / page_size)) + 1):
        yield page


def list_generator(my_list: list, list_size: int, start: int = 1) -> [[]]:
    """
    列表生成器：把一个列表分割成数个小的列表
    :param my_list: 传入的大列表
    :param list_size: 小列表的大小
    :param start: 从第几个列表开始返回，默认从第 1 个
    :return:
    """
    _list = list(my_list)
    for page in range(start, int(ceil(len(_list) / list_size) + 1)):
        yield _list[(page - 1) * list_size: page * list_size]
