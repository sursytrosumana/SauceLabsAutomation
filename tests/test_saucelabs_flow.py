import pytest
from tests.test_saucelabs import SauceLabsTest
from tests.test_data import login_search_data

@pytest.mark.parametrize("data", login_search_data)
def test_search_add_cart_checkout_login_flow(data):
    test = SauceLabsTest()
    try:
        assert test.search_add_cart_checkout_login_flow(
            data["email"],
            data["password"],
            data["search_term"]
        ) is True
    finally:
        test.close_driver()
