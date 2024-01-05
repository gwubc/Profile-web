import time

from selenium import webdriver
import unittest
from pymongo import MongoClient
from selenium.webdriver.common.by import By

HOST_URL = "http://serverundertest:5000"
Webdriver_URL = "http://test-chrome:4444"
Mongo_URL = "mongodb://mongodb:27017/project"


class End_to_End_Test(unittest.TestCase):

    def clear_database(self):
        
        client = MongoClient(Mongo_URL)
         
        db = client["project"]
        collection = db["users"]
        collection.drop()
        client.close()

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Remote(command_executor=Webdriver_URL, options=chrome_options)

    def tearDown(self):
        self.driver.close()
        self.clear_database()

    def _find_text(self, driver, text):
        xpath1 = (f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                  f"'{text.lower()}')]")
        xpath2 = (f"//*[contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                  f"'{text.lower()}')]")

        elements = [x for x in driver.find_elements(By.XPATH, xpath1) if x.is_displayed()]
        elements += [x for x in driver.find_elements(By.XPATH, xpath2) if x.is_displayed()]
        return elements

    def test_text_login(self):
        driver = self.driver
        driver.get(HOST_URL)
        self.assertEqual(len(self._find_text(driver, 'User Login')), 1)
        self.assertEqual(len(self._find_text(driver, 'Username')), 1)
        self.assertEqual(len(self._find_text(driver, 'Password')), 1)
        self.assertEqual(len(self._find_text(driver, 'Login')), 2)
        self.assertEqual(len(self._find_text(driver, 'Register')), 1)
        self.assertEqual(len(self._find_text(driver, 'User Registration')), 0)

    def test_text_register(self):
        driver = self.driver
        driver.get(HOST_URL)
        elements = self._find_text(driver, 'Register')
        self.assertEqual(len(elements), 1)
        elements[0].click()
        time.sleep(0.3)

        self.assertEqual(len(self._find_text(driver, 'User Registration')), 1)
        self.assertEqual(len(self._find_text(driver, 'Username')), 1)
        self.assertEqual(len(self._find_text(driver, 'Password')), 1)
        self.assertEqual(len(self._find_text(driver, 'Login')), 1)
        self.assertEqual(len(self._find_text(driver, 'Register')), 1)
        self.assertEqual(len(self._find_text(driver, 'User Login')), 0)

    def _register(self, driver):
        self._find_text(driver, 'Register')[0].click()
        time.sleep(0.3)
        driver.find_element(By.XPATH, f"//*[contains(@id, 'registerUsername')]").send_keys("testuser")
        driver.find_element(By.XPATH, f"//*[contains(@id, 'registerPassword')]").send_keys("testpass")
        driver.find_element(By.XPATH, f"//*[contains(@value, 'Register')]").click()

    def test_register(self):
        driver = self.driver
        driver.get(HOST_URL)

        self._register(driver)
        time.sleep(0.5)

        self.assertEqual(len(self._find_text(driver, 'Welcome, testuser!')), 1)
        self.assertEqual(len(self._find_text(driver, 'logout')), 1)
        self.assertEqual(len(self._find_text(driver, 'Introduction')), 1)
        self.assertEqual(len(self._find_text(driver, 'Update')), 1)

        self.assertEqual(len(self._find_text(driver, 'User Login')), 0)

    def test_logout_login(self):
        driver = self.driver
        driver.get(HOST_URL)
        time.sleep(0.2)
        self._register(driver)
        time.sleep(0.2)
        self._find_text(driver, 'logout')[0].click()
        time.sleep(0.2)
        self.assertEqual(len(self._find_text(driver, 'User Login')), 1)
        driver.find_element(By.XPATH, f"//*[contains(@id, 'loginUsername')]").send_keys("testuser")
        driver.find_element(By.XPATH, f"//*[contains(@id, 'loginPassword')]").send_keys("testpass")
        driver.find_element(By.XPATH, f"//*[contains(@value, 'Login')]").click()

        self.assertEqual(len(self._find_text(driver, 'Welcome, testuser!')), 1)

    def test_update_introduction(self):
        driver = self.driver
        driver.get(HOST_URL)
        time.sleep(0.2)
        self._register(driver)
        time.sleep(0.2)
        driver.find_element(By.XPATH, f"//*[@id='introduction']").send_keys("some\nintroduction")
        self._find_text(driver, 'Update')[0].click()
        time.sleep(0.2)
        self._find_text(driver, 'logout')[0].click()
        time.sleep(0.2)
        self.assertEqual(len(self._find_text(driver, 'User Login')), 1)
        driver.find_element(By.XPATH, f"//*[contains(@id, 'loginUsername')]").send_keys("testuser")
        driver.find_element(By.XPATH, f"//*[contains(@id, 'loginPassword')]").send_keys("testpass")
        driver.find_element(By.XPATH, f"//*[contains(@value, 'Login')]").click()

        self.assertEqual(len(self._find_text(driver, "some\nintroduction")), 1)


if __name__ == "__main__":
    unittest.main()
