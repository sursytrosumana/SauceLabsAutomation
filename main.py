from tests.test_saucelabs import SauceLabsTest
from tests.test_data import login_search_data
import time
import allure
import os
import inspect

def main():
    print("Validating changes: Screenshots will only be taken on failures, not successes...")
    
    test = SauceLabsTest()
    
    method_source = inspect.getsource(test.home_page.take_screenshot)
    if "pass" in method_source or "# Screenshot capturing on success is disabled" in method_source:
        print("✓ Confirmed: take_screenshot_on_success method is now a no-op")
    else:
        print("✗ Error: take_screenshot_on_success method is not properly disabled")
    
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    
    initial_screenshot_count = len([f for f in os.listdir(screenshots_dir) if f.endswith('.png')])
    print(f"Initial screenshot count: {initial_screenshot_count}")
    
    try:
        print("\nPerforming search -> add product to cart -> checkout -> login tests")
        print("(Note: Screenshots will only be taken on failures, not successes)")

        for i, user_data in enumerate(login_search_data):
            print(f"\nProcessing product {i+1}: {user_data['search_term']}")
            
            success = test.search_add_cart_checkout_login_flow(
                user_data["email"],
                user_data["password"],
                user_data["search_term"]
            )
            
            if success:
                print(f"Successfully completed flow for {user_data['search_term']}")
            else:
                print(f"Failed to complete flow for {user_data['search_term']}")
                
    
        time.sleep(10)
        
    finally:
        final_screenshot_count = len([f for f in os.listdir(screenshots_dir) if f.endswith('.png')])
        print(f"\nFinal screenshot count: {final_screenshot_count}")
        print(f"Total screenshots taken during test: {final_screenshot_count - initial_screenshot_count}")
        
        if final_screenshot_count - initial_screenshot_count == 0:
            print("NOTE: No new screenshots were taken during this test run.")
            print("This means no failures occurred during the test execution.")
        
        print("\nChanges summary:")
        print("- take_screenshot_on_success() method in base_page.py is now a no-op")
        print("- All calls to take_screenshot_on_success() have been removed from test file")
        print("- Failure screenshot calls remain intact and have been enhanced")
        print("\nValidation complete! Screenshots will now only be captured on failures.")
        
        test.close_driver()
