# Import the BasePage class which contains common methods for all pages
from .base_page import BasePage
# Import Allure for test reporting and step tracking
import allure

class ProductPage(BasePage):
    """
    ProductPage class represents the product page of the application.
    It contains locators for elements on the product page and methods to interact with them.
    """
    # Define locators as class constants for elements on the product page
    # Locator for the Add to Cart button
    ADD_TO_CART_BUTTON = "//input[@id='add']"  # Correct XPath according to provided list
    # Locator for product image
    PRODUCT_IMAGE = "//img[@id='feature-image']"  # Correct XPath according to provided list

    def __init__(self, driver):
        """
        Initialize the ProductPage object by calling the parent BasePage constructor.
        
        Args:
            driver: The Selenium WebDriver instance to interact with the browser
        """
        # Call the parent class constructor to initialize the base page functionality
        super().__init__(driver)
        # Store the driver instance (redundant since BasePage already stores it, but kept for clarity)
        self.driver = driver

    @allure.step("Click on product image")
    def click_product_image(self):
        """
        Click on the product image.
        """
        try:
            # Click the product image
            self.click_element(self.PRODUCT_IMAGE)
            # Print confirmation message
            print(f"Clicked on product image")
            return True
        except Exception as e:
            print(f"Could not click on product image: {str(e)}")
            # Alternative: try to find and click the first product image in search results
            try:
                alt_locator = "(//div[contains(@class, 'product-card')]//img)[1]"
                self.click_element(alt_locator)
                print(f"Clicked on alternative product image locator")
                return True
            except:
                print(f"Could not click on alternative product image locator")
                return False

    @allure.step("Add product to cart")
    def add_to_cart(self):
        """
        Add the current product to the cart.
        
        Returns:
            bool: True if product was successfully added to cart, False otherwise
        """
        try:
            # Click the Add to Cart button
            self.click_element(self.ADD_TO_CART_BUTTON)
            # Print confirmation message
            print("Added to cart")
            # Return True to indicate success
            return True
        except Exception as e:
            print(f"Could not add to cart using primary locator: {str(e)}")
            # Try alternative locator for add to cart button
            try:
                alt_locator = "//button[contains(text(), 'Add to cart') or contains(text(), 'ADD TO CART')]"
                self.click_element(alt_locator)
                print("Added to cart using alternative locator")
                return True
            except:
                print("Could not add to cart using alternative locator")
                return False