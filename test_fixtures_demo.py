import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser # yield means above line will execute before all the module
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


def test_goto_google(page):
    page.goto("https://www.google.com/")
    assert "Google" == page.title()


def test_goto_redbus(page):
    page.goto("https://www.redbus.in/")
    assert "Book Bus Tickets Online, Easy & Secure Booking, Top Operators - redBus" == page.title()
