import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
import os
import mysql.connector
import time


class Customer(unittest.TestCase):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_HOST = '192.168.201.14'
    DB_USER = 'wms_icd_staging'
    DB_PASS = 'wms_icd'
    DB_NAME = 'wms_icd_staging'

    def setUp(self):
        # mo trinh duyet
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
        driver = self.driver
        driver.get('http://staging.wms.icd.itlvn.com/customers')
        driver.find_element_by_name('username').send_keys('admin')
        driver.find_element_by_name('password').send_keys('123456')
        warehouse_dropdown = Select(driver.find_element_by_name('warehouse_id'))
        warehouse_dropdown.select_by_value('1')
        driver.find_element_by_id('m_login_signin_submit').click()
        driver.implicitly_wait(10)

    def tearDown(self):
        # dong trinh duyet
        self.driver.close()

    def test_1(self): # kiểm tra sự kiện click link code customer
        driver = self.driver
        driver.find_element_by_css_selector(
            "#customer-data tbody tr:nth-child(1) td:nth-child(1) > a").click()

    def test_click_button_edit(self):
        driver = self.driver
        driver.find_element_by_css_selector("#customer-data tbody tr:nth-child(2) td:nth-child(8)"
                                            " a[title='Edit details']").click()
        time.sleep(3)
        assert "Edit Customer" in driver.page_source

    def test_click_button_delete(self):
        driver = self.driver
        driver.find_element_by_css_selector("#customer-data tbody tr:nth-child(2) td:nth-child(8)"
                                            " a[title='Delete']").click()
        time.sleep(2)
        warning_message = driver.find_element_by_css_selector("#pop-up-delete > div > div > div.modal-body").text
        assert "You are sure delete customer" in warning_message

    def test_click_button_reset(self):
        driver = self.driver
        driver.find_element_by_id('customer-search-reset').click()

    def test_create_customer(self):
        driver = self.driver
        driver.find_element_by_css_selector("a.btn.btn-primary.m-btn.m-btn--icon.m-btn--wide").click()
        assert "Create Customer" in driver.page_source

    def test_import_customer_sucess(self):  # kiểm tra sự kiện click button import
        driver = self.driver
        # Click buton import
        driver.find_element_by_css_selector("a.btn:nth-child(2).btn-primary.m-btn.m-btn--icon.m-btn--wide").click()
        # Chọn file import vào hệ thống
        driver.find_element_by_id('choose-file').send_keys(os.path.abspath("import_customer_sample.xlsx"))
        # Click vào button Upload
        driver.find_element_by_css_selector('#customer-import  div  div  div  div.col-sm-7.col-lg-9.import-form-block'
                                            '  div.clearfix.cta-row  button').click()
        # Chờ cho tới khi xuất hiện 2 dòng dưới lưới import, chờ tối đa 10s
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#customer-data-import > tbody tr[role="row"]')))
        # Lấy những dòng được import
        customer_row_elements = self.driver.find_elements_by_css_selector('#customer-data-import '
                                                                          ' tbody tr[role="row"]')
        # Kiểm tra xem số dòng có bằng 2 hay không
        self.assertEqual(2, len(customer_row_elements), msg="2 dòng customer đã hiện chưa")
        driver.find_element_by_id('btn-list-success').click()
        # Chờ 3s để hiển thị lên popup message
        time.sleep(3)
        # Click vào button Ok trong popup message
        driver.find_element_by_css_selector("#import-success-modal  div  div  div.modal-footer  button").click()
        # Kiểm tra trang đã chuyển sang trang list hay chưa
        WebDriverWait(self.driver, 10).until(expected_conditions.url_to_be
                                             ('http://staging.wms.icd.itlvn.com/customers'))
        # kết nối đến DB warehouuse
        warehouse_db = mysql.connector.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            passwd=self.DB_PASS,
            database=self.DB_NAME
        )
        # Lấy con trỏ trên DB
        warehouse_cursor = warehouse_db.cursor()
        # Query tìm 2 dòng được insert vào DB
        warehouse_cursor.execute(
            "SELECT COUNT(*) FROM customer WHERE (code='TEST01' OR code='Test02')")
        # Lấy số dòng import thành công
        number_of_imported_receipt = warehouse_cursor.fetchone()
        # Kiểm tra xem số dòng import vào DB có phải bằng 2 hay không
        self.assertEqual(2, number_of_imported_receipt[
            0])

    def test_import_customer_error(self):
        pass


if __name__ == "__main__":
    unittest.main()

