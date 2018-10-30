#!/env/bin/python
# encoding: utf-8

from selenium import webdriver
import sys, json
import time

class WebdriverPool(object):
    __pool_size = 2
    __initializd = False
    __drivers = [] # [ [driver_1, availability], [driver_2, availability] ]

    __instance = None

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
                pair = [driver, True]
                self.__drivers.append(pair)
        else:
            pass

    def __get_available_driver_idx(self):
        sn = 0
        while True:
            idx = sn % self.__pool_size
            pair = self.__drivers[idx]
            driver          = pair[0]
            availability    = pair[1]
            print "sn: ", sn
            if availability:
                return idx
            else:
                pass

            if idx == self.__pool_size - 1:
                time.sleep(0.1)

            sn += 1

    def get_html(self, url):
        # get idx
        driver_idx = self.__get_available_driver_idx()

        # get driver
        driver = self.__drivers[driver_idx][0]

        # set driver as busy
        self.__drivers[driver_idx][1] = False
        print driver_idx
        print self.__drivers

        time.sleep(5)
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

        # set driver as available
        self.__drivers[driver_idx][1] = True

        return html

if __name__ == '__main__':
    url = "http://baidu.com"
    wp1 = WebdriverPool()
    wp2 = WebdriverPool()
    import threading
    threading.Thread( target=wp1.get_html, args=(url,) ).start()
    threading.Thread( target=wp2.get_html, args=(url,) ).start()


