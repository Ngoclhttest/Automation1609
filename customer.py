import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

class eWMS(unittest.TestCase):

    def setUp(self): # mo trinh duyet
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
        driver = self.driver
        driver.get('http://staging.wms.icd.itlvn.com/customers')
        driver.find_element_by_name('username').send_keys('admin')
        driver.find_element_by_name('password').send_keys('123456')
        warehouse_dropdown = Select(driver.find_element_by_name('warehouse_id'))
        warehouse_dropdown.select_by_value('1')
        driver.find_element_by_id('m_login_signin_submit').click()
        driver.implicitly_wait(10)

    def tearDown(self): # dong trinh duyet
        self.driver.close()

    def test_1(self): # kiểm tra sự kiện click link code customer
        driver = self.driver
        driver.find_element_by_css_selector(
            "#customer-data tbody tr:nth-child(1) td:nth-child(1) > a").click()

    def test_2(self): # kiểm tra sự kiện click button edit
        driver = self.driver
        driver.find_element_by_css_selector("#customer-data tbody tr:nth-child(2) td:nth-child(8) a[title='Edit details']").click()
        time.sleep(3)
        assert "Edit Customer" in driver.page_source

    def test_3(self):# kiểm tra sự kiện click button delete
        driver = self.driver
        driver.find_element_by_css_selector("#customer-data tbody tr:nth-child(2) td:nth-child(8) a[title='Delete']").click()
        time.sleep(2)
        warning_message = driver.find_element_by_css_selector("#pop-up-delete > div > div > div.modal-body").text
        assert "You are sure delete customer" in warning_message

    def test_4(self): # kiểm tra sự kiện click reset
        driver = self.driver
        driver.find_element_by_id('customer-search-reset').click()

    def test_5(self): # click button create customer
        driver = self.driver
        driver.find_element_by_css_selector("a.btn.btn-primary.m-btn.m-btn--icon.m-btn--wide").click()
        assert "Create Customer" in driver.page_source

    def test_6(self):  # kiểm tra sự kiện click button import
        driver = self.driver
        driver.find_element_by_css_selector("a.btn:nth-child(2).btn-primary.m-btn.m-btn--icon.m-btn--wide").click() # bắt theo class
        assert "Import Customer" in driver.page_source

    def test_7(self): # kiểm tra sự kiện click button export
        driver = self.driver
        driver.find_element_by_css_selector("a.btn:nth-child(3).btn-primary.m-btn.m-btn--icon.m-btn--wide").click()


if __name__ == "__main__":
    unittest.main()

