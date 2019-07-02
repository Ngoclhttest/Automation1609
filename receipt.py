import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
import os
import mysql.connector


class Receipt(unittest.TestCase):
    LOGIN_URL = 'http://staging.wms.icd.itlvn.com/login'
    IMPORT_RECEIPT_URL = 'http://staging.wms.icd.itlvn.com/receipts/import'
    USERNAME = 'admin'
    PASSWORD = '123456'
    WAREHOUSE_ID = '1'
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_HOST = '192.168.201.14'
    DB_USER = 'wms_icd_staging'
    DB_PASS = 'wms_icd'
    DB_NAME = 'wms_icd_staging'

    def setUp(self):
        # Mở trình duyệt
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
        driver = self.driver
        driver.get(self.LOGIN_URL)
        driver.find_element_by_name('username').send_keys(self.USERNAME)
        driver.find_element_by_name('password').send_keys(self.PASSWORD)
        warehouse_dropdown = Select(driver.find_element_by_name('warehouse_id'))
        warehouse_dropdown.select_by_value(self.WAREHOUSE_ID)
        driver.find_element_by_id('m_login_signin_submit').click()
        driver.implicitly_wait(10)

    def tearDown(self):  # Đóng trình duyệt
        self.driver.close()

    def test_import_receipt_success(self):
        # Đổi sang đường dẫn import receipt.
        self.driver.get(self.IMPORT_RECEIPT_URL)
        # Nhét file import sample vào trong nút import.
        self.driver.find_element_by_id('choose-file').send_keys(os.path.abspath("import_receipt_sample.xlsx"))
        # Chờ cho tới khi xuất hiện 2 dòng trên tab Master, chờ tối đa 10s.
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#receipt-master-import > tbody tr[role="row"]')))
        # Lấy những dòng bên tab Master.
        master_row_elements = self.driver.find_elements_by_css_selector('#receipt-master-import > tbody tr[role="row"]')
        # Lấy những dòng bên tab Detail.
        detail_row_elements = self.driver.find_elements_by_css_selector('#receipt-detail-import > tbody tr[role="row"]')
        # Kiểm tra số dòng bên Master có bằng 2 hay không.
        self.assertEqual(2, len(master_row_elements), msg="2 dòng Master đã hiện trên tab Master chưa?")
        # Kiểm tra số dòng bên Detail có bằng 2 hay không.
        self.assertEqual(2, len(detail_row_elements), msg="2 dòng Detail đã hiện trên tab Detail chưa?")
        # Nhấp vào nút Import trên màn hình.
        self.driver.find_element_by_id('btn-pack-list-success').click()
        # Chờ cho tới khi chuyển trang list của Receipt, tối đa 10s.
        WebDriverWait(self.driver, 10).until(expected_conditions.url_to_be('http://staging.wms.icd.itlvn.com/receipts'))
        # Kiểm tra trang đã chuyển là trang Receipt List hay chưa.
        self.assertEqual('http://staging.wms.icd.itlvn.com/receipts', self.driver.current_url)
        """
        Kiểm tra xem trong database đã import thành công chưa bằng cách kiểm tra số lượng record.
        """
        # Kết nối tới database warehouse.
        warehouse_db = mysql.connector.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            passwd=self.DB_PASS,
            database=self.DB_NAME
        )
        # Lấy con trỏ trên database
        warehouse_cursor = warehouse_db.cursor()
        # Query tìm 2 dòng mới được insert vào database.
        warehouse_cursor.execute(
            "SELECT COUNT(*) FROM document WHERE (code='Import1' OR code='Import2') AND type='receipt'")
        # Lấy số dòng import thành công.
        number_of_imported_receipt = warehouse_cursor.fetchone()
        # Kiểm tra số dòng import thành công trong database có phải là 2 hay không.
        self.assertEqual(2, number_of_imported_receipt[
            0])  # number_of_imported_receipt trả về kiểu tuple (2,) nên phải lấy phần tử thứ 0 của tuple đó.


if __name__ == "__main__":
    unittest.main()
