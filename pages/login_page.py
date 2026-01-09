# Import the BasePage class which contains common methods for all pages
from .base_page import BasePage
# Import By class for locating elements using different strategies
from selenium.webdriver.common.by import By
# Import Allure for test reporting and step tracking
import allure

class LoginPage(BasePage):
    """
    LoginPage class represents the login page of the application.
    It contains locators for elements on the login page and methods to interact with them.
    """
    # Define locators as class constants for elements on the login page
    # Locator for the email input field
    EMAIL_INPUT = "//input[@id='customer_email']"  # Correct XPath according to provided list
    # Locator for the password input field
    PASSWORD_INPUT = "//input[@id='customer_password']"  # Correct XPath according to provided list
    # Locator for the Sign In button (input element)
    SIGN_IN_BUTTON = "//input[@type='submit' and @value='Sign In']"  # Correct XPath according to provided list
    
    def __init__(self, driver):
        """
        Initialize the LoginPage object by calling the parent BasePage constructor.
        
        Args:
            driver: The Selenium WebDriver instance to interact with the browser
        """
        # Call the parent class constructor to initialize the base page functionality
        super().__init__(driver)
        # Store the driver instance (redundant since BasePage already stores it, but kept for clarity)
        self.driver = driver

    @allure.step("Enter login credentials")
    def enter_login_credentials(self, email, password):
        """
        Enter login credentials (email and password) into the fields.
        
        Args:
            email (str): The user's email address
            password (str): The user's password
            
        Returns:
            bool: True if both email and password fields were filled, False otherwise
        """
        # Use the email input field
        self.send_keys_to_element(self.EMAIL_INPUT, email)
        # Print confirmation message
        print(f"Email entered: {email}")

        # Use the password input field
        self.send_keys_to_element(self.PASSWORD_INPUT, password)
        # Print confirmation message
        print("Password entered")

        # Return True to indicate both fields were successfully filled
        return True

    @allure.step("Click sign in button")
    def click_sign_in(self):
        """
        Click the Sign In button to submit the login form.
        
        Returns:
            bool: True if Sign In button was successfully clicked, False otherwise
        """
        # Click the Sign In button
        self.click_element(self.SIGN_IN_BUTTON)
        # Print confirmation message
        print("Clicked on Sign In button")
        # Return True to indicate success
        return True