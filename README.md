# Shopping System E2E Test Suite

## Overview
The **Shopping System E2E Test Suite** is an automated end-to-end testing solution built using Playwright and Python. This suite ensures that the core functionalities of the online shopping system are tested and verified. It automates the process of logging in, adding products to the cart, proceeding to checkout, and verifying the order completion.

## Test Coverage
* Logging in with valid credentials.
* Adding two different products to the shopping cart.
* Verifying products in the cart. 
* Proceeding to the checkout and filling in shipping details. 
* Completing the checkout process and verifying the order in the orders page.

## Project Structure
#### Below is the project structure to help you understand how the codebase is organized:
    ShoppingSystemE2E/
    ├── logs/ # Directory to store log files for each test run
    ├── tests/ # Contains the test scripts
    │ └── test_shopping_flow.py # Main E2E test script for the shopping flow
    ├── utils/ # Utility functions and modules
    │ └── logger_setup.py # Logger configuration setup
    ├── .github/ # GitHub Actions configuration
    │ └── workflows/ # CI workflow files
    │    └── e2e_test.yml # Workflow for running the nightly E2E test suite
    ├── .env # Environment variables file (not included in version control)
    ├── requirements.txt # Python dependencies
    └── README.md # Project documentation

## Prerequisites
1. **Python 3.12+**: Ensure you have Python installed.
2. **Node.js**: Playwright requires Node.js for its CLI.
3. **Git**: To clone the repository.
4. **Playwright Browsers**: Install Playwright browsers using:
   ```bash
   playwright install
   
## Get Started

### 1. Clone the repository:
```bash
git clone https://github.com/AlonFriedlander/ShoppingSystemE2E.git
cd ShoppingSystemE2E
```
### 2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Unix systems
.\venv\Scripts\activate   # For Windows systems
```
### 3. Install dependencies:
```bash
pip install -r requirements.txt
```
### 4. Install Playwright browsers:
```bash
playwright install
```
### 5. Create a .env file:
Create a .env file in the project root with the following content(after you register):
```bash
EMAIL=your_email@example.com
PASSWORD=your_password
HEADLESS=False # Set to True for headless mode in CI/CD
```
### 6. Run the Test Suite:
```bash
pytest tests/
```

### 7. Run the Test Suite with console logging:
```bash
pytest -s tests/
```

## Logs
Logs are stored in the logs directory. Each test run creates a log file with a timestamped name.

## CI/CD Integration
This project includes a GitHub Actions workflow for running tests nightly. The workflow runs automatically at 22:30 Israel time.