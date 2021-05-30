import time
import unittest

from selenium import webdriver

from webapp.view import view
from webapp.edit import edit


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('C:\\Users\\User\\Desktop\\test\\chromedriver.exe')
        self.driver.get("http://127.0.0.1:5000")
        time.sleep(2)

    def test_01(self):
        driver = self.driver

        driver.get("http://127.0.0.1:5000/view/table_min_max/")

        time.sleep(3)

        rows = driver.find_elements_by_id('view_row')

        data_view = []

        for row in rows:
            data_view.append(row.text)

        driver.find_element_by_id('link-to-edit-module').click()

        time.sleep(1)

        rows = driver.find_elements_by_id('edit_row')

        data_edit = []

        for row in rows:
            data_edit.append(row.text)

        assert len(data_view) == len(data_edit)

        for i in range(len(data_view)):
            assert data_view[i] == data_edit[i]

    def test_02(self):
        driver = self.driver

        driver.get("http://127.0.0.1:5000/view/Items/")

        time.sleep(3)

        rows = driver.find_elements_by_id('view_row')

        data_view = []

        for row in rows:
            data_view.append(row.text)

        driver.find_element_by_id('link-to-edit-module').click()

        time.sleep(1)

        rows = driver.find_elements_by_id('edit_row')

        data_edit = []

        for row in rows:
            data_edit.append(row.text)

        assert len(data_view) == len(data_edit)

        for i in range(len(data_view)):
            assert data_view[i] == data_edit[i]

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()