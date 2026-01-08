# Import the selenium webdriver module - this allows us to control web browsers
from selenium import webdriver

# Import the By module - this helps us find elements on web pages
from selenium.webdriver.common.by import By

# Import the Service class - this manages the driver executable
from selenium.webdriver.chrome.service import Service

# Import the Options class - this allows us to customize browser settings
from selenium.webdriver.chrome.options import Options

# Import the time module - this lets us add delays between actions
import time

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
def click_element(driver, xpath):
    # Find the element on the page using its XPATH
    element = driver.find_element(By.XPATH, xpath)
    # Click on the found element
    element.click()

# Define a function to enter text into input fields
def send_keys_to_element(driver, xpath, keys):
    # Find the element on the page using its XPATH
    element = driver.find_element(By.XPATH, xpath)
    # Clear any existing text in the field
    element.clear()
    # Enter the new text into the field
    element.send_keys(keys)

# Define test data - this contains login credentials and search terms for testing
login_search_data = [
    # First test case with email, password and search term
    {
        "email": "sumanaghimire45@gmail.com",
        "password": "Sumana@123",
        "search_term": "product"
    },
    # Second test case
    {
        "email": "testuser2@gmail.com",
        "password": "Password2@",
        "search_term": "shirt"
    },
    # Third test case
    {
        "email": "testuser3@gmail.com",
        "password": "Password3#",
        "search_term": "hat"
    }
]

# Function to perform user registration on the website
def perform_registration():
    # Print a message to show registration test is starting
    print("Running registration test with unique email")
    
    # Navigate to the main page before registration
    driver.get('https://sauce-demo.myshopify.com')
    # Wait 2 seconds for the page to load
    time.sleep(2)
    
    # Store the XPATH for the Sign Up link
    SignUp = "//a[contains(text(),'Sign up')]"
    # Click the Sign Up link
    click_element(driver, SignUp)
    # Print a message to confirm the link was clicked
    print("Clicked on Sign up link")

    # Wait 2 seconds for the registration page to load
    time.sleep(2)
    # Check if the registration page loaded by looking at the URL
    if "register" in driver.current_url:
        print("Registration form loaded successfully")
    else:
        print("Warning: Registration form may not have loaded properly - current URL:", driver.current_url)

    # Enter first name into the registration form
    FirstName = "//input[@id='first_name']"
    send_keys_to_element(driver, FirstName, "Test")
    print(f"First name entered: Test")

    # Enter last name into the registration form
    LastName = "//input[@id='last_name']"
    send_keys_to_element(driver, LastName, "User")
    print(f"Last name entered: User")

    # Enter email into the registration form
    Email = "//input[@id='email']"
    # Generate a unique email address each time to avoid duplicate registration
    unique_email = f"testuser_{int(time.time())}@gmail.com"
    send_keys_to_element(driver, Email, unique_email)
    print(f"Unique email entered: {unique_email}")

    # Enter password into the registration form
    Password = "//input[@id='password']"
    send_keys_to_element(driver, Password, "TestPass@123")
    print("Password entered")

    # Click the Create Account button
    CreateButton = "//input[@type='submit' and @value='Create']"
    click_element(driver, CreateButton)
    print("Clicked on Create button")

    # Wait 50 seconds for registration to process
    time.sleep(50) 

    # Check if registration was successful by looking for a logout button
    try:
        # Look for the logout element on the page
        logout_element = driver.find_element(By.XPATH, "//a[text()='Log Out']")
        if logout_element:
            print("Registration successful - Log Out element found")
            return True
    except:
        print("Registration is not successful - No redirect and Log Out element not found")
        return False

# Start the registration process first
print("Performing registration with unique email...")
registration_success = perform_registration()

# Perform login and search tests with the specified credentials
print("\nPerforming login and search tests...")
# Loop through each test case in our test data
#enumerate gives us both the index and the data
#enumerate is built-in function in Python that adds a counter to an iterable and returns it as an enumerate object
for i, user_data in enumerate(login_search_data):
    # Print which test case we're running
    print(f"\nRunning test {i+1} with email: {user_data['email']}, search: {user_data['search_term']}")
    
    # Navigate back to the home page for each test
    driver.get('https://sauce-demo.myshopify.com')
    time.sleep(2)

    # Find and click the login link
    login_link = "//a[@id='customer_login_link']"
    click_element(driver, login_link)
    print("Clicked on Log In link")

    # Wait for navigation to login page
    time.sleep(2)

    # Enter email using the credentials from current test case
    email_input = "//input[@id='customer_email']"
    send_keys_to_element(driver, email_input, user_data["email"])  # Using the email from current iteration
    print(f"Email entered: {user_data['email']}")

    # Enter password using the credentials from current test case
    password_input = "//input[@id='customer_password']"
    send_keys_to_element(driver, password_input, user_data["password"])  # Using the password from current iteration
    print("Password entered")

    # Click Sign In button to submit the login form
    sign_in_button = "//input[@type='submit' and @value='Sign In']"
    click_element(driver, sign_in_button)
    print("Clicked on Sign In button")

    # Wait for potential redirect and page load after login
    time.sleep(500)

    # Search for a product using the search term from current test case
    search_input = "//input[@id='search-field']"
    send_keys_to_element(driver, search_input, user_data["search_term"])
    print(f"Product searched: {user_data['search_term']}")

    # Wait for search results to load
    time.sleep(3)

    # Click on product image to view details
    try:
        product_image = "//img[@id='feature-image']"
        click_element(driver, product_image)
        print("Clicked on product image")
        
        # Wait for product page to load
        time.sleep(3)
        
        # Add product to cart
        add_to_cart_button = "//input[@id='add']"
        click_element(driver, add_to_cart_button)
        print("Added to cart")
        
        # Wait for cart update
        time.sleep(2)
        
        # Click on My Cart link to view cart contents
        my_cart_link = "//a[contains(@class,'toggle-drawer') and contains(@class,'cart')]"
        click_element(driver, my_cart_link)
        print("Clicked on My Cart link")
        
        # Try to get the cart count to see how many items are in the cart
        cart_count_span = "//span[@id='cart-target-desktop']//span"
        try:
            cart_count = driver.find_element(By.XPATH, cart_count_span).text
            print(f"Cart count: {cart_count}")
        except:
            print("Could not find cart count element")
        
        # Click on Check Out link to proceed to checkout
        check_out_link = "//a[@class='checkout']"
        click_element(driver, check_out_link)
        print("Clicked on Check Out link")
        
        # Wait for checkout page to load
        time.sleep(3)
        
        # Click on Check Out submit button to complete the purchase
        check_out_button = "//input[@id='checkout']"
        click_element(driver, check_out_button)
        print("Clicked on Check Out submit button")
        
        # Wait before proceeding to next test
        time.sleep(5)
        
    except Exception as e:
        print(f"Error during product interaction: {str(e)}")
        continue

# Wait 10 seconds before closing the browser to see final results
time.sleep(10)
# Close the browser and end the automation session
driver.quit()
# Print a message to confirm the test is complete
print("All tests completed")

