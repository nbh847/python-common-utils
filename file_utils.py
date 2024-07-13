import os

"""
文件操作类
"""


class FileUtils:
    def __int__(self, file_path: str,  print_log: bool = True):
        """
        param file_path: 文件路径
        param print_log: 是否打印日志，默认是打印
        """
        self.file_path = file_path
        self.print_log = print_log

    def read_line_from_file(self) -> list:
        """
        从文件按行读取数据
        :return:
        """
        if self.print_log:
            print("read from file:{}".format(self.file_path))
        res = []
        with open(self.file_path, "r", encoding="utf8") as f:
            for line in f.readlines():
                if line.strip():
                    res.append(line.strip())
        return res

    def save_to_file(self, data: list, save_type: str = "a+"):
        """
        把数据逐条保存到文件
        :param data: 要保存的数据
        :param save_type: 保存方式，默认是尾行添加
        :return:
        """
        if self.print_log:
            print("save data to file:{}".format(self.file_path))
        with open(self.file_path, save_type, encoding='utf8') as w:
            for item in data:
                w.write(item + '\n')

    def traverse_dir_from_files(self, root_dir: str, ext: str = "") -> ([str], [str]):
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
