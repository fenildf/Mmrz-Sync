#!/env/bin/python
# encoding: utf-8

from selenium import webdriver
import sys, json
import time

class WebdriverPool(object):
    __pool_size = 3
    __instance = None
    __initializd = False
    __drivers = [] # [(driver_1, availability), (driver_2, availability)]

    def __new__(cls, *args, **kw):
        if not cls.__instance:
            cls.__instance = super(WebdriverPool, cls).__new__(cls, *args, **kw)
        return cls.__instance

    def __init__(self):
        if not self.__initializd:
            self.__initializd = True
            for i in range(self.__pool_size):
                driver = webdriver.PhantomJS(service_log_path="{0}/{1}".format(sys.path[0], 'ghostdriver.log'))
                driver.set_page_load_timeout(10)
                driver.set_script_timeout(10)
                self.__drivers.append(driver, True)
        else:
            pass

    def __get_available_driver(self):
        sn = 0
        while True:
            idx = sn % self.__pool_size
            pair = self.__drivers[idx]
            driver          = pair[0]
            availability    = pair[1]
            if availability:
                return driver
            else:
                continue

            if idx == 0:
                time.sleep(0.1)

    def get_html(self, url):
        driver = self.__get_available_driver()
        try:
            driver.get(url)
            driver.refresh()
            html = driver.page_source
        except:
            html = None
        finally:
            # driver.quit()  # quit whole driver
            # driver.close() # close current window
            pass
        return html

if __name__ == '__main__':
    wp1 = WebdriverPool()
    wp2 = WebdriverPool()
    print wp1
    print wp2


