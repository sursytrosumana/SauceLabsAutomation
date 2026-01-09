from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class HomePage(BasePage):
    SIGN_UP_LINK = "//a[contains(text(),'Sign up')]"
    SEARCH_INPUT = "//input[@id='search-field']"
    SEARCH_BUTTON = "//button[@type='submit' and contains(@class, 'icon-search') or contains(@class, 'search-button') or contains(@aria-label, 'Search') or contains(@class, 'search-submit')]"

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Navigate to homepage")
    def navigate_to_home(self):
        self.driver.get('https://sauce-demo.myshopify.com')

    @allure.step("Click on Sign Up link")
    def click_sign_up(self):
        self.click_element(self.SIGN_UP_LINK)

    @allure.step("Search for product: {search_term}")
    def search_product(self, search_term):
        self.send_keys_to_element(self.SEARCH_INPUT, search_term)
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.SEARCH_INPUT)))
        element.send_keys(Keys.RETURN)
        print(f"Product searched: {search_term}")

    @allure.step("Click search button")
    def click_search_button(self):
        try:
            self.click_element(self.SEARCH_BUTTON)
            print("Clicked search button")
        except:
            print("Search button not found or not clickable, search may have already been triggered")

    @allure.step("Click first product in search results")
    def click_first_product_in_search_results(self):
        """
        Click on the first product in the search results.
        Returns:
            bool: True if the first product was successfully clicked, False otherwise
        """
        try:
            # Wait until at least one product is visible
            first_product = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[id^='product-']"))
            )
            first_product.click()
            print("Clicked on the first product successfully")
            return True
        except Exception as e:
            print(f"Failed to click on the first product: {e}")
            return False
