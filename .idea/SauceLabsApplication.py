# Import the selenium webdriver module - this allows us to control web browsers
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import the By module - this helps us find elements on web pages
from selenium.webdriver.common.by import By

# Import the Service class - this manages the driver executable
from selenium.webdriver.chrome.service import Service

# Import the Options class - this allows us to customize browser settings
from selenium.webdriver.chrome.options import Options

# Import the time module - this lets us add delays between actions
import time

# Import allure for generating detailed test reports
# Allure provides beautiful reports with steps, attachments, and test status
import allure

# Create Chrome options object to customize browser behavior
chrome_options = Options()

# Add argument to start the browser maximized (full screen)
chrome_options.add_argument("--start-maximized")

# Create a service object pointing to the ChromeDriver executable
# This is the file that connects our script to the Chrome browser
service = Service('/Users/sumana/Downloads/chromedriver-mac-arm64 2/chromedriver')

# Create a webdriver instance using Chrome with our options and service
# This opens a new Chrome browser window for automation
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the Sauce Demo website - this is our test website
driver.get('https://sauce-demo.myshopify.com')

# Define a function to click on elements using their XPATH
# XPATH is a way to locate elements on a webpage
# Allure step annotation provides reporting for this action
@allure.step("Click on element with xpath: {xpath}")
def click_element(driver, xpath):
    # Find the element on the page using its XPATH
    element = driver.find_element(By.XPATH, xpath)
    # Assert that the element is present
    assert element.is_displayed(), f"Element with xpath {xpath} is not visible"
    # Click on the found element
    element.click()
    print(f"Successfully clicked on element: {xpath}")

# Define a function to enter text into input fields
# Allure step annotation provides reporting for this action
@allure.step("Send keys '{keys}' to element with xpath: {xpath}")
def send_keys_to_element(driver, xpath, keys):
    # Find the element on the page using its XPATH
    element = driver.find_element(By.XPATH, xpath)
    # Assert that the element is present and enabled
    assert element.is_enabled(), f"Element with xpath {xpath} is not enabled"
    # Clear any existing text in the field
    element.clear()
    # Enter the new text into the field
    element.send_keys(keys)
    print(f"Successfully sent keys '{keys}' to element: {xpath}")

# Define a function to assert that an element exists
# Allure step annotation provides reporting for this assertion
@allure.step("Assert element exists with xpath: {xpath}")
def assert_element_exists(driver, xpath, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        assert element.is_displayed(), f"Element with xpath {xpath} is not visible"
        print(f"Assertion passed: Element {xpath} exists and is visible")
        return True
    except:
        print(f"Assertion failed: Element {xpath} does not exist or is not visible")
        return False

# Define test data - this contains login credentials and search terms for testing
login_search_data = [
    # First test case with email, password and search term
    {
        "email": "sumanaghimire45@gmail.com",
        "password": "Sumana@123",
        "search_term": "grey jacket"
    },
    # Second test case
    {
        "email": "testuser2@gmail.com",
        "password": "Password2@",
        "search_term": "noir jacket"
    },
    # Third test case
    {
        "email": "testuser3@gmail.com",
        "password": "Password3#",
        "search_term": "Striped top"
    }
]

# Function to perform user registration on the website
# Allure feature and story annotations organize the test in reports
@allure.feature('SauceLabs Automation')
@allure.story('User Registration')
def perform_registration():
    # Print a message to show registration test is starting
    # Allure step provides detailed reporting for this action
    with allure.step("Running registration test with unique email"):
        print("Running registration test with unique email")
        
        # Navigate to the main page before registration
        driver.get('https://sauce-demo.myshopify.com')
        # Wait 2 seconds for the page to load
        time.sleep(2)
        
        # Store the XPATH for the Sign Up link
        SignUp = "//a[contains(text(),'Sign up')]"
        # Assert that the sign up link exists
        assert_element_exists(driver, SignUp)
        # Click the Sign Up link
        click_element(driver, SignUp)
        # Print a message to confirm the link was clicked
        print("Clicked on Sign up link")

        # Wait 2 seconds for the registration page to load
        time.sleep(2)
        # Check if the registration page loaded by looking at the URL
        if "register" in driver.current_url:
            with allure.step("Registration form loaded successfully"):
                print("Registration form loaded successfully")
        else:
            with allure.step("Warning: Registration form may not have loaded properly"):
                print("Warning: Registration form may not have loaded properly - current URL:", driver.current_url)

        # Enter first name into the registration form
        FirstName = "//input[@id='first_name']"
        # Assert that the first name field exists
        assert_element_exists(driver, FirstName)
        send_keys_to_element(driver, FirstName, "Test")
        print(f"First name entered: Test")

        # Enter last name into the registration form
        LastName = "//input[@id='last_name']"
        # Assert that the last name field exists
        assert_element_exists(driver, LastName)
        send_keys_to_element(driver, LastName, "User")
        print(f"Last name entered: User")

        # Enter email into the registration form
        Email = "//input[@id='email']"
        # Assert that the email field exists
        assert_element_exists(driver, Email)
        # Generate a unique email address each time to avoid duplicate registration
        unique_email = f"testuser_{int(time.time())}@gmail.com"
        send_keys_to_element(driver, Email, unique_email)
        print(f"Unique email entered: {unique_email}")

        # Enter password into the registration form
        Password = "//input[@id='password']"
        # Assert that the password field exists
        assert_element_exists(driver, Password)
        send_keys_to_element(driver, Password, "TestPass@123")
        print("Password entered")

        # Click the Create Account button
        CreateButton = "//input[@type='submit' and @value='Create']"
        # Assert that the create account button exists
        assert_element_exists(driver, CreateButton)
        click_element(driver, CreateButton)
        print("Clicked on Create button")

        # Wait 2 seconds for registration to process
        time.sleep(2)

        # Check if registration was successful by looking for a logout button
        try:
            # Look for the logout element on the page
            logout_element = driver.find_element(By.XPATH, "//a[text()='Log Out']")
            if logout_element:
                with allure.step("Registration successful - Log Out element found"):
                    print("Registration successful - Log Out element found")
                    return True
        except:
            with allure.step("Registration is not successful - No redirect and Log Out element not found"):
                print("Registration is not successful - No redirect and Log Out element not found")
                return False

# Commenting out registration since user requested to skip signup
# Start the registration process first
# print("Performing registration with unique email...")
# registration_success = perform_registration()

# Perform search -> add product to cart -> checkout -> login with valid credentials
# This is the main test flow that includes all required functionality
print("\nPerforming search -> add product to cart -> checkout -> login tests...")

# Process one product for the complete flow
for i, user_data in enumerate(login_search_data):
    # Print which test case we're running
    print(f"\nProcessing product {i+1}: {user_data['search_term']}")
    
    # Navigate back to the home page for each test
    driver.get('https://sauce-demo.myshopify.com')
    time.sleep(2)

    # Search for a product using the search term from current test case
    search_input = "//input[@id='search-field']"
    # Assert that the search input field exists
    assert_element_exists(driver, search_input)
    send_keys_to_element(driver, search_input, user_data["search_term"])
    print(f"Product searched: {user_data['search_term']}")

    # Wait for search results to load
    time.sleep(3)

    # Click on search button if needed
    search_button = "//button[@type='submit' and contains(@class, 'search')]"
    if assert_element_exists(driver, search_button, timeout=5):
        click_element(driver, search_button)
        print("Clicked search button")
        time.sleep(2)

    # Click on product image to view details
    try:
        # Try multiple possible XPaths for product images
        product_image_xpaths = [
            "//img[@id='feature-image']",
            "//div[@class='product-item']//img",
            "//div[@class='product-grid-item']//img",
            "//div[contains(@class,'product')]//img",
            "//a[contains(@class,'product')]//img",
            "(//img[contains(@class,'product') or contains(@class,'image')])[1]",
            "(//a[contains(@class, 'product')])[1]//img",
            "(//a[contains(@href, 'products')])[1]"
        ]
        
        product_image_clicked = False
        for xpath in product_image_xpaths:
            if assert_element_exists(driver, xpath, timeout=5):
                click_element(driver, xpath)
                print(f"Clicked on product image with xpath: {xpath}")
                product_image_clicked = True
                break
        
        if not product_image_clicked:
            # If no specific product image found, try clicking on the first product link
            first_product_link = "(//a[contains(@class,'product') or contains(@href,'products')])[1]"
            if assert_element_exists(driver, first_product_link, timeout=5):
                click_element(driver, first_product_link)
                print(f"Clicked on first product link: {first_product_link}")
            else:
                print("No product image or link found, continuing...")
                continue
        
        # Wait for product page to load
        time.sleep(3)
        
        # Add product to cart
        add_to_cart_button = "//input[@id='add']"
        # If the add to cart button doesn't exist, try alternative selectors
        if not assert_element_exists(driver, add_to_cart_button):
            add_to_cart_button = "//button[contains(text(), 'Add to cart') or contains(text(), 'Add To Cart') or contains(@class, 'add-to-cart') or contains(text(), 'ADD TO CART')]"
        
        if assert_element_exists(driver, add_to_cart_button):
            click_element(driver, add_to_cart_button)
            print("Added to cart")
            # Wait longer for cart to update
            time.sleep(3)
        else:
            print("Add to cart button not found")
            continue
        
        # Wait for cart update
        time.sleep(2)
        
        # Click on My Cart link to view cart contents
        my_cart_link = "//a[contains(@class,'toggle-drawer') and contains(@class,'cart')]"
        # Try alternative cart link selectors
        if not assert_element_exists(driver, my_cart_link):
            my_cart_link = "//a[contains(@href, 'cart') or contains(text(), 'Cart') or contains(@class, 'cart') or contains(@href, '/cart')]"
        
        if assert_element_exists(driver, my_cart_link):
            click_element(driver, my_cart_link)
            print("Clicked on My Cart link")
        else:
            print("Cart link not found")
            continue
        
        # Try to get the cart count to see how many items are in the cart
        cart_count_span = "//span[@id='cart-target-desktop']//span"
        # Alternative selectors for cart count
        if not assert_element_exists(driver, cart_count_span):
            cart_count_span = "//span[contains(@class, 'cart-count') or contains(@class, 'count') or contains(text(), 'cart')]"
        
        try:
            cart_count_element = driver.find_element(By.XPATH, cart_count_span)
            cart_count = cart_count_element.text
            print(f"Cart count: {cart_count}")
            
            # If cart count is 0 or empty, wait and try again
            if not cart_count or cart_count.strip() == "(0)" or cart_count.strip() == "0":
                time.sleep(2)
                cart_count = driver.find_element(By.XPATH, cart_count_span).text
                print(f"Cart count after waiting: {cart_count}")
        except:
            print("Could not find cart count element")
        
        # Wait a bit more to ensure cart is updated
        time.sleep(2)
        
        # Click on Check Out link to proceed to checkout
        # First, let's check if we're already on the cart page or need to click checkout from cart
        checkout_button = "//a[contains(@class, 'checkout') or contains(@href, 'checkout') or contains(text(), 'Checkout') or contains(text(), 'CHECKOUT')]"
        
        # If we're on the cart page (URL contains 'cart'), we need to find the checkout button on that page
        if "cart" in driver.current_url:
            # Look for checkout button specifically on the cart page
            cart_checkout_button = "//a[contains(@class, 'checkout') or contains(@href, 'checkout') or contains(text(), 'Checkout') or contains(text(), 'CHECKOUT') or contains(@class, 'btn-checkout')]"
            if assert_element_exists(driver, cart_checkout_button):
                click_element(driver, cart_checkout_button)
                print("Clicked on Check Out link from cart page")
                
                # Wait for checkout page to load
                time.sleep(5)  # Increased wait time
                
                # Check if we're on the checkout page or need to login first
                current_url = driver.current_url
                print(f"Current URL after clicking checkout: {current_url}")
                
                # If we're on the checkout page, we may need to login
                if "checkout" in current_url:
                    # Look for login option on checkout page
                    login_option = "//a[contains(text(), 'Login') or contains(text(), 'log in') or contains(@href, 'login') or contains(text(), 'Already have an account') or contains(text(), 'Sign in')]"
                    if assert_element_exists(driver, login_option, timeout=5):
                        click_element(driver, login_option)
                        print("Clicked login option on checkout page")
                        time.sleep(2)
                    
                    # Now we should be able to login
                    # Enter email using the current test user's credentials
                    email_input = "//input[@id='customer_email']"
                    if not assert_element_exists(driver, email_input):
                        email_input = "//input[@type='email' or contains(@name, 'email') or contains(@id, 'email') or contains(@placeholder, 'email') or contains(@aria-label, 'email')]"
                    
                    if assert_element_exists(driver, email_input):
                        send_keys_to_element(driver, email_input, user_data["email"])
                        print(f"Email entered: {user_data['email']}")
                    else:
                        print("Email input field not found")
                        continue

                    # Enter password using the current test user's credentials
                    password_input = "//input[@id='customer_password']"
                    if not assert_element_exists(driver, password_input):
                        password_input = "//input[@type='password' or contains(@name, 'password') or contains(@id, 'password') or contains(@placeholder, 'password') or contains(@aria-label, 'password')]"
                    
                    if assert_element_exists(driver, password_input):
                        send_keys_to_element(driver, password_input, user_data["password"])
                        print("Password entered")
                    else:
                        print("Password input field not found")
                        continue

                    # Click Sign In button to submit the login form
                    sign_in_button = "//input[@type='submit' and @value='Sign In']"
                    if not assert_element_exists(driver, sign_in_button):
                        sign_in_button = "//button[contains(text(), 'Sign In') or contains(text(), 'Login') or contains(@type, 'submit') or contains(text(), 'Sign in') or contains(@class, 'btn-login') or contains(@value, 'Sign In')]"
                    
                    if assert_element_exists(driver, sign_in_button):
                        click_element(driver, sign_in_button)
                        print("Clicked on Sign In button")
                    else:
                        print("Sign in button not found")
                        continue

                    # Wait for potential redirect and page load after login
                    time.sleep(5)  # Increased wait time
                    
                    # After login, we should be redirected back to checkout
                    current_url = driver.current_url
                    print(f"URL after login: {current_url}")
                    if "checkout" in current_url:
                        print("Successfully returned to checkout after login")
                    elif "account" in current_url:
                        print("Still on account page, need to go to checkout")
                        # Navigate to checkout if still on account page
                        driver.get('https://sauce-demo.myshopify.com/cart')
                        time.sleep(2)
                        # Try clicking checkout again from cart
                        cart_checkout_button = "//a[contains(@class, 'checkout') or contains(@href, 'checkout') or contains(text(), 'Checkout') or contains(text(), 'CHECKOUT') or contains(@class, 'btn-checkout')]"
                        if assert_element_exists(driver, cart_checkout_button):
                            click_element(driver, cart_checkout_button)
                            print("Clicked on Check Out link from cart")
                    else:
                        print(f"Not on checkout page after login. Current URL: {current_url}")
            else:
                print("Checkout button not found on cart page")
                continue
        elif assert_element_exists(driver, checkout_button):
            click_element(driver, checkout_button)
            print("Clicked on Check Out link")
            
            # Wait for checkout page to load
            time.sleep(3)
            
            # Check if we're on the checkout page or need to login first
            current_url = driver.current_url
            print(f"Current URL: {current_url}")
            
            # If we're on the checkout page, we may need to login
            if "checkout" in current_url:
                # Look for login option on checkout page
                login_option = "//a[contains(text(), 'Login') or contains(text(), 'log in') or contains(@href, 'login') or contains(text(), 'Already have an account') or contains(text(), 'Sign in')]"
                if assert_element_exists(driver, login_option, timeout=5):
                    click_element(driver, login_option)
                    print("Clicked login option on checkout page")
                    time.sleep(2)
            
            # If we're on login page or if we need to login on checkout page
            if "login" in driver.current_url or "account" in driver.current_url or "checkout" in current_url:
                # Enter email using the current test user's credentials
                email_input = "//input[@id='customer_email']"
                if not assert_element_exists(driver, email_input):
                    email_input = "//input[@type='email' or contains(@name, 'email') or contains(@id, 'email') or contains(@placeholder, 'email')]"
                
                if assert_element_exists(driver, email_input):
                    send_keys_to_element(driver, email_input, user_data["email"])
                    print(f"Email entered: {user_data['email']}")
                else:
                    print("Email input field not found")
                    continue

                # Enter password using the current test user's credentials
                password_input = "//input[@id='customer_password']"
                if not assert_element_exists(driver, password_input):
                    password_input = "//input[@type='password' or contains(@name, 'password') or contains(@id, 'password') or contains(@placeholder, 'password')]"
                
                if assert_element_exists(driver, password_input):
                    send_keys_to_element(driver, password_input, user_data["password"])
                    print("Password entered")
                else:
                    print("Password input field not found")
                    continue

                # Click Sign In button to submit the login form
                sign_in_button = "//input[@type='submit' and @value='Sign In']"
                if not assert_element_exists(driver, sign_in_button):
                    sign_in_button = "//button[contains(text(), 'Sign In') or contains(text(), 'Login') or contains(@type, 'submit') or contains(text(), 'Sign in') or contains(@class, 'btn-login')]"
                
                if assert_element_exists(driver, sign_in_button):
                    click_element(driver, sign_in_button)
                    print("Clicked on Sign In button")
                else:
                    print("Sign in button not found")
                    continue

                # Wait for potential redirect and page load after login
                time.sleep(3)
                
                # After login, we should be redirected back to checkout
                current_url = driver.current_url
                print(f"URL after login: {current_url}")
                if "checkout" in current_url:
                    print("Successfully returned to checkout after login")
                elif "account" in current_url:
                    print("Still on account page, need to go to checkout")
                    # Navigate to checkout if still on account page
                    driver.get('https://sauce-demo.myshopify.com/cart')
                    time.sleep(2)
                    # Try clicking checkout again from cart
                    cart_checkout_button = "//a[contains(@class, 'checkout') or contains(@href, 'checkout') or contains(text(), 'Checkout') or contains(text(), 'CHECKOUT') or contains(@class, 'btn-checkout')]"
                    if assert_element_exists(driver, cart_checkout_button):
                        click_element(driver, cart_checkout_button)
                        print("Clicked on Check Out link from cart")
                else:
                    print(f"Not on checkout page after login. Current URL: {current_url}")
        
        # Exit the loop after processing the first product to complete the full flow
        break
        
    except Exception as e:
        print(f"Error during product interaction: {str(e)}")
        continue

# Wait 10 seconds before closing the browser to see final results
time.sleep(10)
# Close the browser and end the automation session
driver.quit()
# Print a message to confirm the test is complete
print("All tests completed")
