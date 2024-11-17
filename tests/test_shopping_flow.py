import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def setup_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

def test_shopping_flow(setup_playwright):
    page = setup_playwright

    # Step 1: Navigate to the website and click on the "Sign In" tab
    page.goto("https://main.d2t1pk7fjag8u6.amplifyapp.com")
    page.click("text='Sign In'")  # Ensure the "Sign In" tab is selected

    # Wait for the "Sign In" form to be visible
    page.wait_for_selector("input[placeholder='Enter your Email']")
    print("Sign in form is visible.")

    # Ensure the "Sign In" tab is still active by checking for a specific attribute or style (optional)
    if not page.is_visible("text='Sign In'.active"):  # Adjust as necessary
        page.click("text='Sign In'")

    # Fill in the login details
    page.fill("input[placeholder='Enter your Email']", "alonf1536@gmail.com")
    page.fill("input[placeholder='Enter your Password']", "Password123!")
    print("Filled in login credentials.")

    # Click the "Sign in" button at the bottom of the form
    page.click("form >> button:has-text('Sign in')")  # Ensure it targets the button within the form
    print("Clicked 'Sign in' button.")

    # Wait for login to complete
    page.wait_for_timeout(5000)

    # Verify we are on a new page after login
    assert page.url != "https://main.d2t1pk7fjag8u6.amplifyapp.com", "Login was not successful; still on the login page."


    # Step 2: Add products to the shopping cart

    # Add Product 1 - $20 to the cart (ensure the selector targets the correct product)
    page.click("xpath=(//div[contains(., 'Product 1 - $20')]//button[contains(text(), 'Add to Cart')])[1]")

    # Add Product 2 - $30 to the cart (ensure the selector targets the correct product)
    page.click("xpath=(//div[contains(., 'Product 2 - $30')]//button[contains(text(), 'Add to Cart')])[2]")

    print("Added Product 1 and Product 2 to the cart.")
    page.wait_for_timeout(2000)  # Short wait to visually check the cart interaction

    # Step 3: Verify that the products were added to the cart
    page.click("text=Shopping Cart")
    page.wait_for_timeout(2000)  # Short wait to visually check the cart interaction
    assert page.is_visible("text=Product 1 - $20"), "Product 1 is not visible in the cart"
    assert page.is_visible("text=Product 2 - $30"), "Product 2 is not visible in the cart"

    # Step 4: Proceed to checkout and fill in shipping information
    page.click("text=Checkout")

    shipping_input = page.wait_for_selector("text=Shipping Address: >> input")

    # Fill in the shipping address
    shipping_input.fill("123 Main St, Metropolis")
    print("Filled in the shipping address.")
    page.wait_for_timeout(2000)

    # Click the Complete Checkout button
    # Step 4: Click the Complete Checkout button and capture the popup message
    page.click("text=Complete Checkout")
    page.wait_for_timeout(2000)

    # Handle the alert dialog and capture the message
    alert_text = page.on("dialog", lambda dialog: dialog.accept() or dialog.message)
    print(f"Captured alert message: {alert_text}")

    # Extract the order ID from the alert message using string manipulation or regex
    order_id = alert_text.split(": ")[1].strip()
    print(f"Captured order ID: {order_id}")

    # Navigate to the Orders page
    page.click("text=Orders")
    page.wait_for_timeout(2000)

    # Verify the order appears in the orders list using the captured order ID
    assert page.is_visible(f"text=Order {order_id}"), "New order not found in orders list"
    print("Order verified successfully!")

