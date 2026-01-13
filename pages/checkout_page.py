# Import the BasePage class which contains common methods for all pages
from .base_page import BasePage
# Import By class for locating elements using different strategies
from selenium.webdriver.common.by import By
# Import Allure for test reporting and step tracking
import allure

class CheckoutPage(BasePage):
    """
    CheckoutPage class represents the checkout page of the application.
    It contains locators for elements on the checkout page and methods to interact with them,
    particularly for the login process during checkout.
    """
    # Define locators as class constants for elements on the checkout page
    # Locator for the login option link on the checkout page
    LOGIN_OPTION = "//a[@id='customer_login_link']"
    # Alternative locator for the login option link on the checkout page
    LOGIN_OPTION_ALT = "//a[contains(text(), 'Log in') or contains(text(), 'Login') or contains(@href, 'login')]"
    # Locator for the email input field
    EMAIL_INPUT = "//input[@id='customer_email']"
    # Alternative locator for the email input field
    EMAIL_INPUT_ALT = "//input[contains(@id, 'email') and contains(@type, 'email')]"
    # Locator for the password input field
    PASSWORD_INPUT = "//input[@id='customer_password']"
    # Alternative locator for the password input field
    PASSWORD_INPUT_ALT = "//input[contains(@id, 'password')]"
    # Locator for the Sign In button (input element)
    SIGN_IN_BUTTON = "//input[@type='submit' and @value='Sign In']"
    # Alternative locator for the Sign In button
    SIGN_IN_BUTTON_ALT = "//input[@type='submit' and contains(@value, 'Sign') or contains(@value, 'Login') or contains(@value, 'In')]"
    # Locator for account verification after login
    ACCOUNT_ELEMENT = "//div[contains(@class, 'account') or contains(@class, 'dashboard') or contains(@class, 'profile') or contains(@class, 'customer')]"
    # Alternative locator for account verification after login
    ACCOUNT_ELEMENT_ALT = "//*[contains(text(), 'Welcome') or contains(text(), 'Account') or contains(text(), 'Hello')]"
    
    def __init__(self, driver):
        """
        Initialize the CheckoutPage object by calling the parent BasePage constructor.
        
        Args:
            driver: The Selenium WebDriver instance to interact with the browser
        """
        # Call the parent class constructor to initialize the base page functionality
        super().__init__(driver)
        # Store the driver instance (redundant since BasePage already stores it, but kept for clarity)
        self.driver = driver

    @allure.step("Click login option on checkout page")
    def click_login_option(self):
        """
        Click the login option link on the checkout page.
        
        Returns:
            bool: True if login option was successfully clicked, False otherwise
        """
        try:
            # Try the primary login option
            self.click_element(self.LOGIN_OPTION)
            # Print confirmation message
            print("Clicked login option on checkout page")
            # Return True to indicate success
            return True
        except:
            try:
                # If the primary locator fails, try the alternative
                self.click_element(self.LOGIN_OPTION_ALT)
                # Print confirmation message
                print("Clicked alternative login option on checkout page")
                # Return True to indicate success
                return True
            except Exception as e:
                # Take screenshot on failure
                self.take_screenshot("click_login_option_failure")
                print(f"Failed to click login option: {e}")
                return False

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
        try:
            # Use the primary email input field
            self.send_keys_to_element(self.EMAIL_INPUT, email)
            # Print confirmation message
            print(f"Email entered: {email}")
        except:
            try:
                # If the primary locator fails, try the alternative
                self.send_keys_to_element(self.EMAIL_INPUT_ALT, email)
                # Print confirmation message
                print(f"Email entered using alternative field: {email}")
            except Exception as e:
                # Take screenshot on failure
                self.take_screenshot("enter_email_failure")
                print(f"Failed to enter email: {e}")
                return False
        
        try:
            # Use the primary password input field
            self.send_keys_to_element(self.PASSWORD_INPUT, password)
            # Print confirmation message
            print("Password entered")
        except:
            try:
                # If the primary locator fails, try the alternative
                self.send_keys_to_element(self.PASSWORD_INPUT_ALT, password)
                # Print confirmation message
                print("Password entered using alternative field")
            except Exception as e:
                # Take screenshot on failure
                self.take_screenshot("enter_password_failure")
                print(f"Failed to enter password: {e}")
                return False
        
        # Return True to indicate both fields were successfully filled
        return True

    @allure.step("Click sign in button")
    def click_sign_in(self):
        """
        Click the Sign In button to submit the login form.
        
        Returns:
            bool: True if Sign In button was successfully clicked, False otherwise
        """
        try:
            # Try the primary sign in button
            self.click_element(self.SIGN_IN_BUTTON)
            # Print confirmation message
            print("Clicked on Sign In button")
            # Return True to indicate success
            return True
        except:
            try:
                # If the primary locator fails, try the alternative
                self.click_element(self.SIGN_IN_BUTTON_ALT)
                # Print confirmation message
                print("Clicked on alternative Sign In button")
                # Return True to indicate success
                return True
            except Exception as e:
                # Take screenshot on failure
                self.take_screenshot("click_sign_in_failure")
                print(f"Failed to click sign in button: {e}")
                return False
    
    @allure.step("Verify login success")
    def verify_login_success(self):
        """
        Verify that login was successful by checking for account-related elements.
        
        Returns:
            bool: True if login appears successful, False otherwise
        """
        try:
            # Try to find the primary account element
            element_found = self.assert_element_exists(self.ACCOUNT_ELEMENT, timeout=5)
            if element_found:
                print("Login verified as successful - account element found")
                return True
        except:
            try:
                # If the primary locator fails, try the alternative
                element_found = self.assert_element_exists(self.ACCOUNT_ELEMENT_ALT, timeout=5)
                if element_found:
                    print("Login verified as successful - alternative account element found")
                    return True
            except:
                print("Login may not have been successful - account element not found")
                return False
        
        print("Login may not have been successful - account element not found")
        return False