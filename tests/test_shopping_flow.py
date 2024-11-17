import pytest
from playwright.sync_api import sync_playwright
import sys
import os
import random
from dotenv import load_dotenv, find_dotenv


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger_setup import logger

# Load environment variables from .env
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

# Get email and password from environment variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Check if EMAIL or PASSWORD are not set
if not EMAIL or not PASSWORD:
    logger.error("Email or password not found in the .env file. Please set them.")
    raise ValueError("Email or password not found in the .env file. Please set them.")


@pytest.fixture(scope="module")
def setup_playwright():
    headless_mode = os.getenv("HEADLESS", "True").lower() == "true"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless_mode)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()


def test_shopping_flow(setup_playwright):
    page = setup_playwright

    # Step 1: Navigate to the website and click on the "Sign In" tab
    page.goto("https://main.d2t1pk7fjag8u6.amplifyapp.com")
    page.click("text='Sign In'")  # Ensure the "Sign In" tab is selected
    page.wait_for_selector("input[placeholder='Enter your Email']")
    logger.info("Sign in form is visible.")

    if not page.is_visible("text='Sign In'.active"):
        page.click("text='Sign In'")

    # Fill in the login details
    page.fill("input[placeholder='Enter your Email']", EMAIL)
    page.fill("input[placeholder='Enter your Password']", PASSWORD)
    logger.info("Filled in login credentials.")
    page.click("form >> button:has-text('Sign in')")  # Ensure it targets the button within the form
    logger.info("Clicked 'Sign in' button.")

    # Verify we are on a new page after login
    assert page.url != "https://main.d2t1pk7fjag8u6.amplifyapp.com", "Login failed."

    # Step 2: Randomly select 2 different products to add to the cart
    selected_products = random.sample(range(1, 6), 2)  # Randomly select 2 unique product numbers

    for product_id in selected_products:
        page.click(
            f"xpath=(//div[contains(., 'Product {product_id}')]//button[contains(text(), 'Add to Cart')])[{product_id}]")
        logger.info(f"Added Product {product_id} to the cart.")

    # Step 3: Verify that the selected products were added to the cart
    page.click("text=Shopping Cart")
    for product_id in selected_products:
        assert page.is_visible(f"text=Product {product_id}"), f"Product {product_id} is not visible in the cart"
    logger.info("Selected products are visible in the cart.")

    # Step 4: Proceed to checkout
    page.click("text=Checkout")

    shipping_input = page.wait_for_selector("text=Shipping Address: >> input")

    # Fill in the shipping address
    shipping_input.fill("dizengoff center")
    logger.info("Shipping address filled.")

    # Step 5: Complete checkout and capture order ID
    captured_message = None

    def handle_dialog(dialog):
        nonlocal captured_message
        captured_message = dialog.message
        dialog.accept()

    # Set up the dialog event listener
    page.once("dialog", handle_dialog)
    page.click("text=Complete Checkout")
    page.wait_for_timeout(3000)  # Wait to ensure the dialog is captured

    # Check if the alert message was captured correctly
    if captured_message:
        logger.info(f"Captured alert message: {captured_message}")
        order_id = captured_message.split(": ")[1].strip()
        logger.info(f"Captured order ID: {order_id}")
    else:
        logger.error("No alert message captured")
        raise Exception("No alert message captured")

    # Step 6: Verify order on the Orders page
    page.click("text=Orders")
    page.wait_for_timeout(2000)
    assert page.is_visible(f"text=Order {order_id}"), "New order not found in orders list"
    logger.info("Order verified successfully!")
