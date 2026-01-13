from .base_page import BasePage
import allure

class ProductPage(BasePage):
    ADD_TO_CART_BUTTON = "//input[@id='add']"
    PRODUCT_IMAGE = "//img[@id='feature-image']"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("Click on product image")
    def click_product_image(self):
        try:
            self.click_element(self.PRODUCT_IMAGE)
            print(f"Clicked on product image")
            return True
        except Exception as e:
            self.take_screenshot("click_product_image_failure")
            print(f"Could not click on product image: {str(e)}")
            try:
                alt_locator = "(//div[contains(@class, 'product-card')]//img)[1]"
                self.click_element(alt_locator)
                print(f"Clicked on alternative product image locator")
                return True
            except:
                self.take_screenshot("click_alt_product_image_failure")
                print(f"Could not click on alternative product image locator")
                return False

    @allure.step("Add product to cart")
    def add_to_cart(self):
        try:
            self.click_element(self.ADD_TO_CART_BUTTON)
            print("Added to cart")
            return True
        except Exception as e:
            self.take_screenshot("add_to_cart_failure")
            print(f"Could not add to cart using primary locator: {str(e)}")
            try:
                alt_locator = "//button[contains(text(), 'Add to cart') or contains(text(), 'ADD TO CART')]"
                self.click_element(alt_locator)
                print("Added to cart using alternative locator")
                return True
            except:
                self.take_screenshot("add_to_cart_alt_failure")
                print("Could not add to cart using alternative locator")
                return False