import os
import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura de pantalla automática en caso de fallo"""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        driver = item.funcargs["driver"]
        screenshot = driver.get_screenshot_as_base64()
        html = (
            f'<div><img src="data:image/png;base64,{screenshot}" alt="screenshot" '
            f'style="width:304px;height:228px;" onclick="window.open(this.src)" '
            f'align="right"/></div>'
        )
        extras.append(pytest_html.extras.html(html))
        report.extras = extras


@pytest.fixture
def driver():
    """Fixture del navegador (headless solo en CI)"""
    options = Options()
    en_ci = bool(os.environ.get("CI"))

    if en_ci:
        options.add_argument("--headless=new")  # Ejecución sin ventana
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    if not en_ci:
        driver.maximize_window()

    yield driver
    driver.quit()