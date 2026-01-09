# Import the BasePage class which contains common methods for all pages
from .base_page import BasePage
# Import Allure for test reporting and step tracking
import allure
# Import time module for adding delays in the automation
import time

class RegistrationPage(BasePage):
    """
    RegistrationPage class represents the registration page of the application.
    It contains locators for elements on the registration page and methods to interact with them.
    """
    # Define locators as class constants for elements on the registration page
    # Locator for the first name input field
    FIRST_NAME_INPUT = "//input[@id='first_name']"  # Correct XPath according to provided list
    # Locator for the last name input field
    LAST_NAME_INPUT = "//input[@id='last_name']"  # Correct XPath according to provided list
    # Locator for the email input field
    EMAIL_INPUT = "//input[@id='email']"  # Correct XPath according to provided list
    # Locator for the password input field
    PASSWORD_INPUT = "//input[@id='password']"  # Correct XPath according to provided list
    # Locator for the Create Account button
    CREATE_ACCOUNT_BUTTON = "//input[@type='submit' and @value='Create']"  # Correct XPath according to provided list
    # Locator for the Logout element (used to verify successful registration)
    LOGOUT_ELEMENT = "//a[text()='Log Out']"  # Correct XPath according to provided list

    def __init__(self, driver):
        """
        Initialize the RegistrationPage object by calling the parent BasePage constructor.
        
        Args:
            driver: The Selenium WebDriver instance to interact with the browser
        """
        # Call the parent class constructor to initialize the base page functionality
        super().__init__(driver)
        # Store the driver instance (redundant since BasePage already stores it, but kept for clarity)
        self.driver = driver

    @allure.step("Fill registration form")
    def fill_registration_form(self, first_name, last_name, email, password):
        """
        Fill the registration form with the provided user details.
        
        Args:
            first_name (str): The user's first name
            last_name (str): The user's last name
            email (str): The user's email address
            password (str): The user's password
        """
        # Enter first name into the corresponding input field
        self.send_keys_to_element(self.FIRST_NAME_INPUT, first_name)
        # Print confirmation message
        print(f"First name entered: {first_name}")

        # Enter last name into the corresponding input field
        self.send_keys_to_element(self.LAST_NAME_INPUT, last_name)
        # Print confirmation message
        print(f"Last name entered: {last_name}")

        # Enter email into the corresponding input field
        self.send_keys_to_element(self.EMAIL_INPUT, email)
        # Print confirmation message
        print(f"Email entered: {email}")

        # Enter password into the corresponding input field
        self.send_keys_to_element(self.PASSWORD_INPUT, password)
        # Print confirmation message
        print("Password entered")

    @allure.step("Click create account button")
    def click_create_account(self):
        """
        Click the Create Account button to submit the registration form.
        """
        # Click the Create Account button using BasePage method
        self.click_element(self.CREATE_ACCOUNT_BUTTON)
        # Print confirmation message
        print("Clicked on Create button")
        # Wait 2 seconds for registration to process (allow time for server-side operations)
        time.sleep(2)  # Wait for registration to process

    @allure.step("Verify registration success")
    def verify_registration_success(self):
        """
        Verify if the registration was successful by checking for the presence of the Logout element.
        
        Returns:
            bool: True if registration was successful (Logout element found), False otherwise
        """
        try:
            # Import By class for locating elements using different strategies
            from selenium.webdriver.common.by import By
            # Look for the logout element on the page to confirm successful registration
            logout_element = self.driver.find_element(By.XPATH, self.LOGOUT_ELEMENT)
            # Check if the logout element exists
            if logout_element:
                # Print success message
                print("Registration successful - Log Out element found")
                # Return True indicating successful registration
                return True
        except:
            # Print failure message if registration was not successful
            print("Registration is not successful - No redirect and Log Out element not found")
            # Return False indicating unsuccessful registration
            return False