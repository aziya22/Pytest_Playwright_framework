import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="module")
def browser_handle():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page_handle(browser_handle):
    page = browser_handle.new_page()
    yield page
    page.close()


@pytest.mark.parametrize('invalid_user_name, invalid_password', [('admin', 'Admin1'), ('sgjfas', 'asutwuq')])
def test_invalid_login(page_handle,invalid_user_name,invalid_password):
    page_handle.goto('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
    page_handle.wait_for_selector('//input[@name="username"]').type(invalid_user_name)
    page_handle.wait_for_selector('//input[@name="password"]').type(invalid_password)
    page_handle.wait_for_selector('//button[@type="submit"]').click()

    page_handle.wait_for_timeout(3000)
    error_message = page_handle.wait_for_selector('//div[@role="alert"]//p').text_content()
    assert "Invalid credentials" == error_message
