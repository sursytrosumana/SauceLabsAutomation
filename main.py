# Import the main test class from the test module
from tests.test_saucelabs import SauceLabsTest
# Import test data from the test data module
from tests.test_data import login_search_data
# Import time module for adding delays in the automation
import time
# Import Allure for test reporting and step tracking
import allure

def main():
    """
    Main function to execute the Sauce Labs automation tests.
    Creates a test instance and runs the search -> add to cart -> checkout -> login flow.
    """
    # Create an instance of the SauceLabsTest class
    test = SauceLabsTest()
    
    try:
        # Perform search -> add product to cart -> checkout -> login with valid credentials
        # This is the main test flow that includes all required functionality
        print("\nPerforming search -> add product to cart -> checkout -> login tests")

        # Process one product for the complete flow
        # Loop through each user data in the test data list
        for i, user_data in enumerate(login_search_data):
            # Print which test case we're running
            print(f"\nProcessing product {i+1}: {user_data['search_term']}")
            
            # Execute the main flow with current user data
            # This performs search, add to cart, checkout, and login operations
            success = test.search_add_cart_checkout_login_flow(
                user_data["email"],      # User's email for login
                user_data["password"],   # User's password for login
                user_data["search_term"] # Product to search for
            )
            
            # Check if the test flow was successful
            if success:
                # Print success message
                print(f"Successfully completed flow for {user_data['search_term']}")
            else:
                # Print failure message
                print(f"Failed to complete flow for {user_data['search_term']}")
                

        # Wait 10 seconds before closing the browser to see final results
        time.sleep(10)
        
    finally:
        # Always close the driver at the end, regardless of success or failure
        # This ensures the browser is properly closed and resources are freed
        test.close_driver()

# Check if this script is being run directly (not imported)
# If so, execute the main function
if __name__ == "__main__":
    main()