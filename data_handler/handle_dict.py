from __future__ import annotations


# ------ dict -----
class DictHandler:
    """
    get value from dict
    """

    def __init__(self, dict_obj: dict):
        if not isinstance(dict_obj, dict):
            raise Exception("type of the input object is not dict")
        self.dict_obj = dict_obj

    def get_int(self, key: str | int, default=None):
        """
        format int
        :param key:
        :param default:
        :return: int
        """
        return int(self.dict_obj.get(key)) if (self.dict_obj.get(key) or self.dict_obj.get(key) == 0) else default

    def get_float(self, key: str, default=None):
        """
        format float
        :param key:
        :param default:
        :return:
        """
        return float(self.dict_obj.get(key)) if (self.dict_obj.get(key) or self.dict_obj.get(key) == 0) else default

    def get_str(self, key: str, default=None):
        """
        format str
        :param key:
        :param default:
        :return:
        """
        return str(self.dict_obj.get(key)).strip() if self.dict_obj.get(key) else default

    def get_array(self, key: str, default=None):
        """
        format array
        :param key:
        :param default:
        :return:
        """
        return list(self.dict_obj.get(key)) if self.dict_obj.get(key) else default

    def get_nested_dict(self, key: str, default=None):
        """
        format array
        :param key:
        :param default:
        :return:
        """
        return DictHandler(dict(self.dict_obj.get(key))) if self.dict_obj.get(key) else default

    def filter_matched_array(self, key: str, default=None):
        """
        format array
        :param key:
        :param default:
        :return:
        """
        result = []
        for _key, _value in self.dict_obj.items():
            if _key.startswith(key):
                result.append(_value)
        return result if result else default
