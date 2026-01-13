from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure
import os

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Click on element with xpath: {xpath}")
    def click_element(self, xpath):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            assert element.is_displayed(), f"Element with xpath {xpath} is not visible"
            element.click()
            print(f"Successfully clicked on element: {xpath}")
        except Exception as e:
            element_name = xpath.split('/')[-1].replace('"', '').replace("'", "")
            self.take_screenshot(f"click_failure_{element_name}")
            raise e

    @allure.step("Send keys '{keys}' to element with xpath: {xpath}")
    def send_keys_to_element(self, xpath, keys):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            assert element.is_enabled(), f"Element with xpath {xpath} is not enabled"
            element.clear()
            element.send_keys(keys)
            print(f"Successfully sent keys '{keys}' to element: {xpath}")
        except Exception as e:
            element_name = xpath.split('/')[-1].replace('"', '').replace("'", "")
            self.take_screenshot(f"send_keys_failure_{element_name}")
            raise e

    @allure.step("Assert element exists with xpath: {xpath}")
    def assert_element_exists(self, xpath, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            element = self.driver.find_element(By.XPATH, xpath)
            assert element.is_displayed(), f"Element with xpath {xpath} is not visible"
            print(f"Assertion passed: Element {xpath} exists and is visible")
            return True
        except Exception as e:
            element_name = xpath.split('/')[-1].replace('"', '').replace("'", "")
            self.take_screenshot(f"element_exists_failure_{element_name}")
            print(f"Assertion failed: Element {xpath} does not exist or is not visible")
            return False

    @allure.step("Wait for element to be visible: {xpath}")
    def wait_for_element(self, xpath, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            element_name = xpath.split('/')[-1].replace('"', '').replace("'", "")
            self.take_screenshot(f"wait_element_failure_{element_name}")
            raise e

    @allure.step("Get element text: {xpath}")
    def get_element_text(self, xpath):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return element.text
        except Exception as e:
            element_name = xpath.split('/')[-1].replace('"', '').replace("'", "")
            self.take_screenshot(f"get_text_failure_{element_name}")
            raise e

    @allure.step("Take screenshot: {name}")
    def take_screenshot(self, name="screenshot", timestamp=True):
        #Timestamp avoids file overwrite issues when tests fail multiple times.
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        
        import time
        if timestamp:
            timestamp_str = int(time.time())
            filename = f"{screenshots_dir}/{name}_{timestamp_str}.png"
        else:
            filename = f"{screenshots_dir}/{name}.png"
        
        self.driver.save_screenshot(filename)
        
        allure.attach.file(
            filename,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        print(f"Screenshot taken: {filename}")
