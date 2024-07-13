import os
from configparser import ConfigParser


class CustomConfigParser(ConfigParser):
    CONST_ENV_DEV = 'dev'
    CONST_ENV_TEST = 'test'
    CONST_ENV_PRODUCT = 'product'

    def __init__(self, *args, **kwargs):
        self.__process_name = 'unknow'
        super().__init__(*args, **kwargs)

    def is_product(self):
        return self.get('app', 'env') == 'product'

    def is_test(self):
        return self.get('app', 'env') == 'test'

    def is_dev(self):
        return self.get('app', 'env') == 'dev'


os.environ['TZ'] = 'Asia/Shanghai'
config = CustomConfigParser()
config.read('conf/app.ini', 'utf-8')
