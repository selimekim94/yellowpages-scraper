from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from sys import platform
from selenium.common.exceptions import TimeoutException


class WebDriver:

    def __init__(self, opts=None):
        self.opts = opts
        if platform == "linux" or platform == "linux2":
            self.driver = webdriver.Chrome('./chromedriver/chromedriver', chrome_options=opts)
        elif platform == "darwin":
            self.driver = webdriver.Chrome('./chromedriver/chromedriver', chrome_options=opts)
        elif platform == "win32":
            self.driver = webdriver.Chrome('./chromedriver/chromedriver.exe', chrome_options=opts)
        self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(30)
        self.driver.set_script_timeout(30)

    def wait_until_page_loaded(self):
        return WebDriverWait(self.driver, 30).until(lambda driver:
                                                    driver.execute_script('return document.readyState'))

    def wait_until_ajax_response(self):
        return WebDriverWait(self.driver, 30).until(lambda driver:
                                                    driver.execute_script(
                                                        'return !!window.jQuery && jQuery.active == 0'))

    def wait_until_page_url(self, url):
        return WebDriverWait(self.driver, 30).until(lambda driver:
                                                    driver.current_url.startswith(url))

    def wait_until_page_url_not(self, url):
        return WebDriverWait(self.driver, 30).until(lambda driver:
                                                    not driver.current_url.startswith(url))

    def wait_until_page_url_ends_with(self, url):
        return WebDriverWait(self.driver, 30).until(lambda driver:
                                                    driver.current_url.endswith(url))

    def send_slow_key(self, element=None, keys=None):
        for key in keys:
            element.send_keys(key)
            time.sleep(0.1)

    def wait_element(self, by=None, element=None):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((by, element)))
        except TimeoutException:
            raise

    def get_element(self, by=None, element=None):
        return self.driver.find_element(by, element)

    def get_elements(self, by=None, element=None):
        return self.driver.find_elements(by, element)

    def get_current_url(self):
        return self.driver.current_url

    def get_parent_node(self, by=None, element=None, n=1):
        element = self.get_element(by, element)
        repeated_str = ''
        for i in range(n):
            repeated_str = repeated_str + '.parentNode'
        script = 'return arguments[0]{};'.format(repeated_str)
        return self.driver.execute_script(script, element)
