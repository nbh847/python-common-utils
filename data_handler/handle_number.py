from typing import Any


# ------ number -----
def deep_float_formatter(data: Any):
    """
    深度格式化一个数据结构里的所有浮点型数字
    :param data:
    :return:
    """
    if isinstance(data, list):
        for item in data:
            yield from deep_float_formatter(item)
    elif isinstance(data, dict):
        for value in data.values():
            yield from deep_float_formatter(value)
    else:
        yield format_float(data)


def format_float(value):
    if not isinstance(value, (int, float)):
        return value
    return round(value, 2)


if __name__ == '__main__':
    data = ["sdf", 1, 234.44455, "sdf", "22", {"age": 12}, ["xi", "ha", 23, 23.3411]]
    for i in deep_float_formatter(data):
        print(i)
