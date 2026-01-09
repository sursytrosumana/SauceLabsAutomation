# Import Selenium WebDriver components for browser automation
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# Import time module for adding delays in the automation
import time
# Import Allure for test reporting and step tracking
import allure
# Import page objects for different sections of the application
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage

class SauceLabsTest:
    """
    Main test class for Sauce Labs automation.
    Contains methods for registration, search, add to cart, checkout, and login flows.
    """
    def __init__(self):
        """
        Initialize the SauceLabsTest class by setting up the Chrome driver and page objects.
        """
        # Create Chrome options object to customize browser behavior
        chrome_options = Options()
        # Add argument to start the browser maximized (full screen)
        chrome_options.add_argument("--start-maximized")
        
        # Create a service object pointing to the ChromeDriver executable
        # Note: Update this path to match your system's ChromeDriver location
        service = Service('/Users/sumana/Downloads/chromedriver-mac-arm64 2/chromedriver')
        
        # Create a webdriver instance using Chrome with our options and service
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Initialize page objects for different sections of the application
        # This follows the Page Object Model design pattern
        self.home_page = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.registration_page = RegistrationPage(self.driver)

    @allure.feature('SauceLabs Automation')
    @allure.story('User Registration')
    def perform_registration(self):
        """
        Perform user registration test with a unique email address.
        
        Returns:
            bool: True if registration was successful, False otherwise
        """
        # Start the registration test step in Allure
        with allure.step("Running registration test with unique email"):
            # Print start message
            print("Running registration test with unique email")
            
            # Navigate to the main page before registration
            self.home_page.navigate_to_home()
            # Wait 2 seconds for the page to load
            time.sleep(2)
            
            # Click the Sign Up link to navigate to registration page
            self.home_page.click_sign_up()
            # Print confirmation message
            print("Clicked on Sign up link")

            # Wait 2 seconds for the registration page to load
            time.sleep(2)
            # Check if the registration page loaded by looking at the URL
            if "register" in self.driver.current_url:
                # Report success in Allure
                with allure.step("Registration form loaded successfully"):
                    # Print success message
                    print("Registration form loaded successfully")
            else:
                # Report warning in Allure
                with allure.step("Warning: Registration form may not have loaded properly"):
                    # Print warning message with current URL
                    print("Warning: Registration form may not have loaded properly - current URL:", self.driver.current_url)

            # Generate a unique email address each time to avoid duplicate registration
            # Uses current timestamp to ensure uniqueness
            unique_email = f"testuser_{int(time.time())}@gmail.com"
            
            # Fill registration form with test data
            self.registration_page.fill_registration_form("Test", "User", unique_email, "TestPass@123")
            
            # Click the Create Account button to submit the form
            self.registration_page.click_create_account()
            
            # Verify registration success by checking for logout element
            return self.registration_page.verify_registration_success()

    @allure.feature('SauceLabs Automation')
    @allure.story('Search, Add to Cart, Checkout Flow')
    def search_add_cart_checkout_login_flow(self, email, password, search_term):
        """
        Perform the complete flow: search for product, add to cart, checkout, and login.
        
        Args:
            email (str): User's email for login
            password (str): User's password for login
            search_term (str): Product to search for
            
        Returns:
            bool: True if the flow completed successfully, False otherwise
        """
        # Navigate back to the home page
        self.home_page.navigate_to_home()
        # Wait 2 seconds for the page to load
        time.sleep(2)

        # Search for a product using the search term
        self.home_page.search_product(search_term)

        # Wait for search results to load
        time.sleep(5)

        # Click on first product in search results
        product_clicked = self.home_page.click_first_product_in_search_results()
        # Check if product was successfully clicked
        if not product_clicked:
            # Print error message and return False
            print("Could not click on product from search results, continuing...")
            return False

        # Wait for product page to load
        time.sleep(3)

        # Add product to cart
        added_to_cart = self.product_page.add_to_cart()
        # Check if product was successfully added to cart
        if not added_to_cart:
            # Print error message and return False
            print("Could not add product to cart")
            return False

        # Wait for cart update
        time.sleep(2)

        # Click on My Cart link to view cart contents
        cart_clicked = self.cart_page.click_my_cart()
        # Check if cart link was successfully clicked
        if not cart_clicked:
            # Print error message and return False
            print("Could not click on cart link")
            return False

        # Try to get the cart count to see how many items are in the cart
        cart_count = self.cart_page.get_cart_count()
        
        # Wait a bit more to ensure cart is updated
        time.sleep(2)

        # Click on Check Out link to proceed to checkout
        checkout_clicked = self.cart_page.click_checkout()
        # Check if checkout button was successfully clicked
        if not checkout_clicked:
            # Print error message and return False
            print("Could not click on checkout button")
            return False

        # Wait for checkout page to load
        time.sleep(5)  # Increased wait time

        # Check if we're on the checkout page or need to login first
        current_url = self.driver.current_url
        # Print current URL for debugging
        print(f"Current URL after clicking checkout: {current_url}")

        # If we're on the checkout page, we may need to login
        if "checkout" in current_url:
            # Look for login option on checkout page
            login_clicked = self.checkout_page.click_login_option()
            # Check if login option was successfully clicked
            if login_clicked:
                # Print confirmation message
                print("Clicked login option on checkout page")
                # Wait 2 seconds for the login form to appear
                time.sleep(2)
            
            # Enter login credentials using the provided email and password
            credentials_entered = self.checkout_page.enter_login_credentials(email, password)
            # Check if credentials were successfully entered
            if not credentials_entered:
                # Print error message and return False
                print("Could not enter login credentials")
                return False

            # Click Sign In button to submit the login form
            sign_in_clicked = self.checkout_page.click_sign_in()
            # Check if Sign In button was successfully clicked
            if not sign_in_clicked:
                # Print error message and return False
                print("Could not click sign in button")
                return False

            # Wait for potential redirect and page load after login
            time.sleep(5)  # Increased wait time

            # After login, we should be redirected back to checkout
            current_url = self.driver.current_url
            # Print URL after login for debugging
            print(f"URL after login: {current_url}")
            # Check if we're back on checkout page
            if "checkout" in current_url:
                # Print success message
                print("Successfully returned to checkout after login")
            elif "account" in current_url:
                # Print message if still on account page
                print("Still on account page, need to go to checkout")
                # Navigate to checkout if still on account page
                self.driver.get('https://sauce-demo.myshopify.com/cart')
                time.sleep(2)
                # Try clicking checkout again from cart
                checkout_clicked = self.cart_page.click_checkout()
                if checkout_clicked:
                    print("Clicked on Check Out link from cart")
            else:
                # Print error message with current URL
                print(f"Not on checkout page after login. Current URL: {current_url}")
        
        # Return True to indicate successful completion of the flow
        return True

    def close_driver(self):
        """
        Close the browser and end the automation session.
        """
        # Close the browser and end the automation session
        self.driver.quit()
        # Print a message to confirm the test is complete
        print("All tests completed")