from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service('/Users/sumana/Downloads/chromedriver-mac-arm64 2/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://sauce-demo.myshopify.com')

def click_element(driver, xpath):
    element = driver.find_element(By.XPATH, xpath)
    element.click()

def send_keys_to_element(driver, xpath, keys):
    element = driver.find_element(By.XPATH, xpath)
    element.clear()
    element.send_keys(keys)

# Navigate to the registration page
SignUp = "//a[contains(text(),'Sign up')]"
click_element(driver, SignUp)
print("Clicked on Sign up link")

# Wait for navigation to registration page
time.sleep(2)
# Verify registration page opens properly by checking the URL
if "register" in driver.current_url:
    print("Registration form loaded successfully")
else:
    print("Warning: Registration form may not have loaded properly - current URL:", driver.current_url)

FirstName = "//input[@id='first_name']"
send_keys_to_element(driver, FirstName, "Sumana")
print("First name entered")

LastName = "//input[@id='last_name']"
send_keys_to_element(driver, LastName, "Ghimire")
print("Last name entered")

Email = "//input[@id='email']"
# Generate a unique email address each time
# time.time() Comes from Python's built-in time module
# It returns the current time in seconds since Jan 1, 1970
# int(time.time()) Converts that floating-point number into an integer.
# f" ... " This is an f-string (formatted string). It lets you insert Python expressions directly inside {}.
# testuser_{int(time.time())}@gmail.com" The timestamp is inserted into the email string.

unique_email = f"testuser_{int(time.time())}@gmail.com"
send_keys_to_element(driver, Email, unique_email)
print("Email entered")

Password = "//input[@id='password']"
send_keys_to_element(driver, Password, "sumana@123")
print("Password entered")

CreateButton = "//input[@type='submit' and @value='Create']"
click_element(driver, CreateButton)
print("Clicked on Create button")

# Assert that registration was successful by checking the URL first, then for the presence of the Log Out element
time.sleep(5)  # Wait for potential redirect and page load

# Check if redirected to account page first (primary indicatorot redirected, check for the presence of the Log Out element as secondary indicato
logout_element = driver.find_element(By.XPATH, "//a[text()='Log Out']")
if logout_element:
    print("Registration successful - Log Out element found")
else:
    print("Registration is not successful - No redirect and Log Out element not found")
  
time.sleep(60)
driver.quit()
