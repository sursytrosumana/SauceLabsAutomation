from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import allure
from pages.search_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.signup import RegistrationPage

class SauceLabsTest:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        service = Service('/Users/sumana/Downloads/chromedriver-mac-arm64 2/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.home_page = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.registration_page = RegistrationPage(self.driver)

    @allure.feature('SauceLabs Automation')
    @allure.story('User Registration')
    def perform_registration(self):
        with allure.step("Running registration test with unique email"):
            print("Running registration test with unique email")
            self.home_page.navigate_to_home()
            time.sleep(2)
            self.home_page.click_sign_up()
            print("Clicked on Sign up link")
            time.sleep(2)
            
            if "register" in self.driver.current_url:
                with allure.step("Registration form loaded successfully"):
                    print("Registration form loaded successfully")
            else:
                with allure.step("Warning: Registration form may not have loaded properly"):
                    print("Warning: Registration form may not have loaded properly - current URL:", self.driver.current_url)

            unique_email = f"testuser_{int(time.time())}@gmail.com"
            self.registration_page.fill_registration_form("Test", "User", unique_email, "TestPass@123")
            self.registration_page.click_create_account()
            
            success = self.registration_page.verify_registration_success()
            if not success:
                self.registration_page.take_screenshot("registration_failure")
            return success

    @allure.feature('SauceLabs Automation')
    @allure.story('Search, Add to Cart, Checkout Flow')
    def search_add_cart_checkout_login_flow(self, email, password, search_term):
        self.home_page.navigate_to_home()
        time.sleep(2)
        
        # Verify we're on the home page
        if "sauce-demo" not in self.driver.current_url:
            self.home_page.take_screenshot("homepage_navigation_failure")
            print("Failed to navigate to homepage")
            return False
            
        self.home_page.search_product(search_term)
        time.sleep(5)

        product_clicked = self.home_page.click_first_product_in_search_results()
        if not product_clicked:
            self.home_page.take_screenshot("click_product_failure")
            print("Could not click on product from search results, continuing...")
            return False

        time.sleep(3)
        added_to_cart = self.product_page.add_to_cart()
        if not added_to_cart:
            self.product_page.take_screenshot("add_to_cart_failure")
            print("Could not add product to cart")
            return False

        time.sleep(2)
        cart_clicked = self.cart_page.click_my_cart()
        if not cart_clicked:
            self.cart_page.take_screenshot("click_cart_failure")
            print("Could not click on cart link")
            return False

        time.sleep(2)
        checkout_clicked = self.cart_page.click_checkout()
        if not checkout_clicked:
            self.cart_page.take_screenshot("click_checkout_failure")
            print("Could not click on checkout button")
            return False

        time.sleep(5)
        current_url = self.driver.current_url
        print(f"Current URL after clicking checkout: {current_url}")

        if "checkout" not in current_url:
            self.cart_page.take_screenshot("checkout_navigation_failure")
            print("Failed to navigate to checkout page")
            return False

        login_clicked = self.checkout_page.click_login_option()
        if not login_clicked:
            self.checkout_page.take_screenshot("click_login_option_failure")
            print("Could not click login option on checkout page")
            return False
        
        credentials_entered = self.checkout_page.enter_login_credentials(email, password)
        if not credentials_entered:
            self.checkout_page.take_screenshot("enter_credentials_failure")
            print("Could not enter login credentials")
            return False

        sign_in_clicked = self.checkout_page.click_sign_in()
        if not sign_in_clicked:
            self.checkout_page.take_screenshot("click_sign_in_failure")
            print("Could not click sign in button")
            return False

        time.sleep(5)
        login_verified = self.checkout_page.verify_login_success()
        current_url = self.driver.current_url
        print(f"URL after login: {current_url}")
        
        if "checkout" in current_url or login_verified:
            print("Successfully returned to checkout after login")
        elif "account" in current_url:
            print("Still on account page, need to go to checkout")
            self.driver.get('https://sauce-demo.myshopify.com/cart')
            time.sleep(2)
            checkout_clicked = self.cart_page.click_checkout()
            if checkout_clicked:
                print("Clicked on Check Out link from cart")
        else:
            print(f"Not on checkout page after login. Current URL: {current_url}")
            # Take a screenshot showing the current page state after failed login
            self.checkout_page.take_screenshot("post_login_state_unexpected")
            return False
    
        return True

    def close_driver(self):
        self.driver.quit()
        print("All tests completed")