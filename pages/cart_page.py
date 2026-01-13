# Import the BasePage class which contains common methods for all pages
from .base_page import BasePage
# Import By class for locating elements using different strategies
from selenium.webdriver.common.by import By
# Import Allure for test reporting and step tracking
import allure

class CartPage(BasePage):
    # Define locators as class constants for elements on the cart page
    # Locator for the My Cart link
    MY_CART_LINK = "//a[contains(@class,'toggle-drawer') and contains(@class,'cart')]"  
    # Locator for the checkout button
    CHECKOUT_BUTTON = "//a[@class='checkout']"  
    
    def __init__(self, driver):
        """
        Initialize the CartPage object by calling the parent BasePage constructor.
        
        Args:
            driver: The Selenium WebDriver instance to interact with the browser
        """
        # Call the parent class constructor to initialize the base page functionality
        super().__init__(driver)


    @allure.step("Click on My Cart link")
    def click_my_cart(self):
        """
        Click on the cart link to navigate to the shopping cart page.
        
        Returns:
            bool: True if cart link was successfully clicked, False otherwise
        """
        # Click the cart link
        self.click_element(self.MY_CART_LINK)
        # Print confirmation message
        print("Clicked on My Cart link")
        # Return True to indicate success
        return True

    @allure.step("Click on checkout button")
    def click_checkout(self):
        """
        Click the checkout button to proceed to the checkout process.
        
        Returns:
            bool: True if checkout button was successfully clicked, False otherwise
        """
        # Click the checkout button
        self.click_element(self.CHECKOUT_BUTTON)
        # Print confirmation message
        print("Clicked on Check Out link")
        # Return True to indicate success
        return True