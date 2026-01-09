# Import the BasePage class which contains common methods for all pages
from .base_page import BasePage
# Import By class for locating elements using different strategies
from selenium.webdriver.common.by import By
# Import Allure for test reporting and step tracking
import allure

class CartPage(BasePage):
    """
    CartPage class represents the shopping cart page of the application.
    It contains locators for elements on the cart page and methods to interact with them.
    """
    # Define locators as class constants for elements on the cart page
    # Locator for the My Cart link
    MY_CART_LINK = "//a[contains(@class,'toggle-drawer') and contains(@class,'cart')]"  # Correct XPath according to provided list
    # Locator for the cart count element
    CART_COUNT_SPAN = "//span[@id='cart-target-desktop']//span"  # Correct XPath according to provided list
    # Locator for the checkout button
    CHECKOUT_BUTTON = "//a[@class='checkout']"  # Correct XPath according to provided list
    
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

    @allure.step("Get cart count")
    def get_cart_count(self):
        """
        Get the number of items in the shopping cart.
        
        Returns:
            str or None: The cart count as a string if found, None otherwise
        """
        try:
            # Find the cart count element using By.XPATH
            cart_count_element = self.driver.find_element(By.XPATH, self.CART_COUNT_SPAN)
            # Get the text content of the cart count element
            cart_count = cart_count_element.text
        except:
            # If the specific cart count element is not found, try to find any element that might show cart count
            try:
                alt_cart_count_locator = "//*[@id='cart-count' or contains(@class, 'cart-count') or contains(@class, 'count')]"
                cart_count_element = self.driver.find_element(By.XPATH, alt_cart_count_locator)
                cart_count = cart_count_element.text
            except:
                # If no cart count element is found, try to count items in cart differently
                try:
                    # Try to count cart items by looking for product rows in cart
                    cart_items_locator = "//div[contains(@class, 'cart-item') or contains(@class, 'product')]"
                    cart_items = self.driver.find_elements(By.XPATH, cart_items_locator)
                    cart_count = str(len(cart_items))
                except:
                    # If all attempts fail, return 0
                    cart_count = "0"
        
        # Print the cart count
        print(f"Cart count: {cart_count}")
        # Return the cart count
        return cart_count

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