import random
import time
import uuid
from copy import deepcopy

from data_handler.handle_string import merge_str


def generator_random_id():
    """create new random id"""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + '.' + str(random.random())))


# ------ data structure -----
class ListToTree:
    def __init__(self, data: iter):
        self.__data = deepcopy(list(data))
        self.__primary_key = 'id'
        self.__parent_key = 'parentId'
        self.__children_key = 'children'
        self.__root_id = None
        self.__leaf_ids = None

    def get_children_tree(self):
        return self.__build().get(self.__children_key, [])

    def get_tree(self):
        return self.__build()

    def set_primary_key(self, primary_key):
        self.__primary_key = primary_key
        return self

    def set_parent_key(self, parent_key):
        self.__parent_key = parent_key
        return self

    def set_children_key(self, children_key):
        self.__children_key = children_key
        return self

    def set_root_id(self, root_id):
        self.__root_id = root_id
        return self

    def set_leaf_ids(self, leaf_ids):
        self.__leaf_ids = leaf_ids
        return self

    def __build(self):
        if self.__leaf_ids is not None and not self.__leaf_ids:
            return {}

        data = self.__data
        # filter leaf nodes, get nodes from leaf up to root
        if self.__leaf_ids:
            data_dict = dict((_['menuId'], _) for _ in data)
            effect_node_ids = set()
            for _node_id in self.__leaf_ids:
                while True:
                    if _node_id in effect_node_ids or _node_id not in data_dict:
                        break
                    effect_node_ids.add(_node_id)
                    _node_id = data_dict.get(_node_id, {}).get(self.__parent_key)
            data = filter(lambda x: x['menuId'] in effect_node_ids, self.__data)
        if not data:
            return {}

        root_node = None
        if self.__root_id:
            for _ in data:
                if _[self.__primary_key] == self.__root_id:
                    root_node = _
            if not root_node:
                return {}

        children_list_assoc = {}
        for _ in data:
            children_list_assoc.setdefault(_[self.__parent_key], []).append(_)
        return self.__recursive(children_list_assoc, root_node)

    def __recursive(self, children_list_assoc, node=None):
        """
        recursive to build tree
        :param children_list_assoc:
        :param node:
        :return:
        """
        if not children_list_assoc:
            return node
        if not node:
            # find root node
            for _ in ['', -1, '0']:
                if _ in children_list_assoc:
                    node = {self.__primary_key: _}
                    break
            if not node:
                raise Exception('not found root node')
        if node[self.__primary_key] not in children_list_assoc:
            return node
        node.setdefault(self.__children_key, [])
        for _ in children_list_assoc.pop(node[self.__primary_key]):
            if _[self.__primary_key] in children_list_assoc:
                node[self.__children_key].append(self.__recursive(children_list_assoc, _))
            else:
                node[self.__children_key].append(_)
        return node


class TreeToList:
    def __init__(self, tree):
        self.__data = deepcopy(tree)
        self.__primary_key = 'id'
        self.__parent_key = 'parentId'
        self.__children_key = 'children'
        self.__generator_id_function = None

    def get_list(self):
        return self.__build()

    def set_primary_key(self, primary_key):
        self.__primary_key = primary_key
        return self

    def set_parent_key(self, parent_key):
        self.__parent_key = parent_key
        return self

    def set_children_key(self, children_key):
        self.__children_key = children_key
        return self

    def set_generator_id_function(self, generator_id_function):
        self.__generator_id_function = generator_id_function
        return self

    def __build(self):
        data = self.__data
        if isinstance(data, dict):
            return self.__recursive([data], data.get(self.__parent_key))
        else:
            return self.__recursive(data)

    def __recursive(self, children: iter, parent_id=None):
        """
        recursive to build list
        :param children:
        :param parent_id:
        :return:
        """
        if not children:
            return []
        data_list = []
        for _ in children:
            if parent_id is not None:
                _[self.__parent_key] = parent_id
            if not _.get(self.__primary_key):
                _[self.__primary_key] = self.__generator_id()
            data_list.append(_)
            if self.__children_key in _:
                _children = _.pop(self.__children_key)
                data_list.extend(self.__recursive(_children, _[self.__primary_key]))
        return data_list

    def __generator_id(self):
        if self.__generator_id_function:
            return self.__generator_id_function()
        return generator_random_id()


class ListMergeToDict:
    CONST_DEFAULT_KEY = ''
    """
    把list 合并成dict
    :return: target_dict{v0:{k2:v2, k3:v3+v33}}
    """

    def __init__(self, source_list: iter, primary_keys: iter):
        """
        :param list source_list: [{k0:v1, k2:v2, k3:v3},{k1:v1, k2:v2, k3:v33}] 源列表
        :param list primary_keys: ['k0'] or None 生成主键的key
        """
        self.__source_list = source_list
        self.__primary_keys = primary_keys
        self.__retain_keys = None
        self.__sum_keys = None
        self.__min_keys = None
        self.__max_keys = None

    def get_result(self):
        result = {}
        for row in self.__source_list:
            key = merge_str(*(row[_] for _ in self.__primary_keys)) if self.__primary_keys else self.CONST_DEFAULT_KEY
            result.setdefault(key, {})
            if self.__retain_keys:
                for _key, _value in self.__get_key_value(self.__retain_keys):
                    if row.get(_value):
                        result[key][_key] = row.get(_value)

            if self.__min_keys:
                for _key, _value in self.__get_key_value(self.__min_keys):
                    if row.get(_value) and row.get(_value) > -1:
                        result[key].setdefault(_key, row.get(_value))
                        result[key][_key] = min(result[key][_key], row.get(_value))

            if self.__max_keys:
                for _key, _value in self.__get_key_value(self.__max_keys):
                    if row.get(_value) and row.get(_value) > -1:
                        result[key][_key] = max(result[key].get(_key, -1), row.get(_value))

            if self.__sum_keys:
                for _key, _value in self.__get_key_value(self.__sum_keys):
                    result[key].setdefault(_key, -1)
                    result[key][_key] += int(row.get(_value, -1))
        if self.__primary_keys:
            return result
        else:
            return result.get(self.CONST_DEFAULT_KEY, {})

    def get_result_list(self):
        return list(self.get_result().values())

    def set_retain_keys(self, keys):
        """
        设置 保留的key
        :param keys:
        :return:
        """
        self.__retain_keys = keys
        return self

    def set_sum_keys(self, keys):
        """
        设置 求和的key
        :param keys:
        :return:
        """
        self.__sum_keys = keys
        return self

    def set_min_keys(self, keys):
        """
        设置 求最小 -1不参与
        :param keys:
        :return:
        """
        self.__min_keys = keys
        return self

    def set_max_keys(self, keys):
        """
        设置 求最大 默认-1
        :param keys:
        :return:
        """
        self.__max_keys = keys
        return self

    def __get_key_value(self, keys):
        """
        get key value
        :param keys:
        :return:
        """
        if isinstance(keys, dict):
            for _key, _value in keys.items():
                yield _key, _value
        else:
            for _key in keys:
                if isinstance(_key, tuple):
                    yield _key[-1], _key[1]
                else:
                    yield _key, _key
