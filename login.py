import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time


class EWMS(unittest.TestCase):

    def setUp(self):  # mo trinh duyet
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
        driver = self.driver
        driver.get('http://staging.wms.icd.itlvn.com')
        assert "Login - eWMS" in driver.title

    def tearDown(self):  # dong trinh duyet
        self.driver.close()

    def testcase1(self):
        pass

    def testcase2(self):  # login success
        driver = self.driver
        driver.find_element_by_name('username').send_keys('admin')
        driver.find_element_by_name('password').send_keys('123456')
        warehouse_dropdown = Select(driver.find_element_by_name('warehouse_id'))
        warehouse_dropdown.select_by_value('1')
        driver.find_element_by_id('m_login_signin_submit').click()
        assert "List Customer" in driver.page_source

    def testcase3(self):  # login without pass
        driver = self.driver
        driver.find_element_by_name('username').send_keys('admin')
        warehouse_dropdown = Select(driver.find_element_by_name('warehouse_id'))
        warehouse_dropdown.select_by_value('1')
        driver.find_element_by_id('m_login_signin_submit').click()
        assert "Value is required and can't be empty" in driver.page_source

    def testcase4(self):  # login without user
        driver = self.driver
        driver.find_element_by_name('password').send_keys('123456')
        warehouse_dropdown = Select(driver.find_element_by_name('warehouse_id'))
        warehouse_dropdown.select_by_value('1')
        driver.find_element_by_id('m_login_signin_submit').click()
        assert "Value is required and can't be empty" in driver.page_source

    def testcase5(self):  # error user and pass
        driver = self.driver
        driver.find_element_by_name('username').send_keys('add')
        driver.find_element_by_name('password').send_keys('111111')
        warehouse_dropdown = Select(driver.find_element_by_name('warehouse_id'))
        warehouse_dropdown.select_by_value('1')


if __name__ == "__main__":
    unittest.main()
