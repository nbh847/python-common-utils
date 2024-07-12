import os

"""
文件操作类
"""


def read_line_from_file(file_path: str) -> list:
    """
    从文件按行读取数据
    :param file_path:
    :return:
    """
    print("read from file:{}".format(file_path))
    res = []
    with open(file_path, "r", encoding="utf8") as f:
        for line in f.readlines():
            if line.strip():
                res.append(line.strip())
    return res


def save_to_file(file_path: str, data: list, save_type: str = "a+", print_log: bool = True):
    """
    把数据逐条保存到文件
    :param file_path:
    :param data:
    :param save_type: 保存方式，默认是尾行添加
    :param print_log: 是否打印日志，默认是打印
    :return:
    """
    if print_log:
        print("save data to file:{}".format(file_path))
    with open(file_path, save_type, encoding='utf8') as w:
        for item in data:
            w.write(item + '\n')


def traverse_dir_files(root_dir: str, ext: str = "") -> ([str], [str]):
    """
    列出文件夹中的所有文件，深度遍历
    :param root_dir: 根目录
    :param ext: 后缀名
    :return: [文件路径列表，文件名称列表]
    """
    names_list = []
    paths_list = []
    for parent, _, file_names in os.walk(root_dir):
        for name in file_names:
            if name.startswith("."):  # 去除隐藏文件
                continue
            if ext:  # 根据后缀名搜索
                if name.endswith(tuple(ext)):
                    names_list.append(name)
                    paths_list.append(os.path.join(parent, name))
            else:
                names_list.append(name)
                paths_list.append(os.path.join(parent, name))
    return paths_list, names_list
