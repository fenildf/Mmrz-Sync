#!/env/bin/python
# encoding: utf-8

from selenium import webdriver
import json

class WebdriverPool(object):
    __instance = None
    __initializd = False

    def __new__(cls, *args, **kw):
        if not cls.__instance:
            cls.__instance = super(WebdriverPool, cls).__new__(cls, *args, **kw)
        return cls.__instance

    def __init__(self):
        if not self.__class__.__initializd:
            self.__class__.__initializd = True
            self.driver = webdriver.PhantomJS(service_log_path="{0}/{1}".format(sys.path[0], 'ghostdriver.log'))
            self.driver.set_page_load_timeout(10)
            self.driver.set_script_timeout(10)
        else:
            pass


if __name__ == '__main__':
    wp1 = WebdriverPool()
    wp2 = WebdriverPool()
    print wp1
    print wp2


