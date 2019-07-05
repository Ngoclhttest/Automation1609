import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

class eWMS(unittest.TestCase):

    def setUp(self): # mo trinh duyet
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
        driver = self.driver
        driver.get('http://staging.wms.icd.itlvn.com/categories')
        driver.implicitly_wait(10)
        driver.find_element_by_name('username').send_keys('admin')
        driver.find_element_by_name('password').send_keys('123456')
        warehouse_dropdown = Select(driver.find_element_by_name('warehouse_id'))
        warehouse_dropdown.select_by_value('1')
        driver.find_element_by_id('m_login_signin_submit').click()

    def test_link_category(self): # kiểm tra sự kiện click vào link name
        driver = self.driver
        driver.find_element_by_css_selector(
            "#category-data > tbody > tr:nth-child(2) > td.text-center.sorting_1 > a").click()
        assert "DR" in driver.page_source

    def test_click_bt_create(self):  # kiểm tra sự kiện click bt create category
        driver = self.driver
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='List Category'])[1]/following::i[1]").click()
        assert "Add Category" in driver.page_source

    def test_click_edit(self): # Kiểm tra sự kiện khi click icon edit
        driver =self.driver
        driver.find_element_by_css_selector(
            "#category-data > tbody > tr:nth-child(1) > td:nth-child(4) > a:nth-child(1)").click()
        assert "Edit Category" in driver.page_source

    def test_click_delete(self): # Kiểm tra sự kiện khi click icon delete
        driver = self.driver
        driver.implicitly_wait(50)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='Thức uống'])[1]/following::i[2]").click()
        time.sleep(1)
        warning_message = driver.find_element_by_css_selector("#delete-confirm-modal > div > div > div.modal-body.text-center").text
        assert "Do you want to delete this category?" in warning_message

    def tearDown(self): # dong trinh duyet
        self.driver.close()


if __name__ == "__main__":
    unittest.main()