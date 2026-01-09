# Import necessary Selenium libraries for web automation
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
# Import Allure for test reporting and step tracking
import allure

class BasePage:
    """
    BasePage class serves as a parent class for all page objects in the automation framework.
    It contains common methods that can be reused across different pages like clicking elements,
    sending keys, waiting for elements, etc.
    """
    def __init__(self, driver):
        """
        Initialize the BasePage with a web driver instance.
        
        Args:
            driver: The Selenium WebDriver instance to interact with the browser
        """
        self.driver = driver  # Store the driver instance
        self.wait = WebDriverWait(driver, 10)  # Set up a wait object with 10 second timeout

    @allure.step("Click on element with xpath: {xpath}")
    def click_element(self, xpath):
        """
        Click on an element after waiting for it to be clickable.
        
        Args:
            xpath (str): The XPath locator of the element to click
            
        Raises:
            AssertionError: If the element is not visible when clicked
        """
        # Wait until the element is clickable using the provided XPath
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        # Verify that the element is displayed before clicking
        assert element.is_displayed(), f"Element with xpath {xpath} is not visible"
        # Perform the click action
        element.click()
        # Print a confirmation message
        print(f"Successfully clicked on element: {xpath}")

    @allure.step("Send keys '{keys}' to element with xpath: {xpath}")
    def send_keys_to_element(self, xpath, keys):
        """
        Send text to an input field after waiting for it to be clickable.
        
        Args:
            xpath (str): The XPath locator of the input field
            keys (str): The text to send to the input field
            
        Raises:
            AssertionError: If the element is not enabled when sending keys
        """
        # Wait until the element is clickable using the provided XPath
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        # Verify that the element is enabled before sending keys
        assert element.is_enabled(), f"Element with xpath {xpath} is not enabled"
        # Clear any existing text in the input field
        element.clear()
        # Send the specified keys to the input field
        element.send_keys(keys)
        # Print a confirmation message
        print(f"Successfully sent keys '{keys}' to element: {xpath}")

    @allure.step("Assert element exists with xpath: {xpath}")
    def assert_element_exists(self, xpath, timeout=10):
        """
        Check if an element exists on the page within a specified timeout.
        
        Args:
            xpath (str): The XPath locator of the element to check
            timeout (int): Maximum time to wait for the element (default: 10 seconds)
            
        Returns:
            bool: True if element exists and is visible, False otherwise
        """
        try:
            # Wait for the element to be present using WebDriverWait
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            # Find the element once it's located
            element = self.driver.find_element(By.XPATH, xpath)
            # Verify that the element is displayed
            assert element.is_displayed(), f"Element with xpath {xpath} is not visible"
            # Print success message
            print(f"Assertion passed: Element {xpath} exists and is visible")
            # Return True indicating the element exists
            return True
        except:
            # Print failure message if element is not found or not visible
            print(f"Assertion failed: Element {xpath} does not exist or is not visible")
            # Return False indicating the element doesn't exist
            return False

    @allure.step("Wait for element to be visible: {xpath}")
    def wait_for_element(self, xpath, timeout=10):
        """
        Wait for an element to be visible on the page.
        
        Args:
            xpath (str): The XPath locator of the element to wait for
            timeout (int): Maximum time to wait for the element (default: 10 seconds)
            
        Returns:
            WebElement: The element once it becomes visible
        """
        # Wait until the element is visible using the provided XPath
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    @allure.step("Get element text: {xpath}")
    def get_element_text(self, xpath):
        """
        Get the text content of an element after waiting for it to be present.
        
        Args:
            xpath (str): The XPath locator of the element to get text from
            
        Returns:
            str: The text content of the element
        """
        # Wait until the element is located using the provided XPath
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        # Return the text content of the element
        return element.text