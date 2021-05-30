# -*- coding: utf-8 -*-
from behave import *
from selenium import webdriver
import unittest
import time

from selenium.webdriver.common.keys import Keys


class SystemTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('C:\\Users\\User\\Desktop\\test\\chromedriver.exe')
        self.driver.get("http://127.0.0.1:5000")

    def test_view_headers_count(self):
        driver = self.driver

        driver.find_element_by_id('link-to-view-module').click()

        time.sleep(3)

        headers = driver.find_elements_by_name('header_title')

        assert len(headers) == 7

    def test_edit_module_window(self):
        driver = self.driver

        driver.find_element_by_id('link-to-view-module').click()

        time.sleep(3)

        driver.find_element_by_id('link-to-edit-module').click()

        time.sleep(2)

        driver.find_element_by_id('edit_icon').click()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
