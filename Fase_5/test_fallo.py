from login_page import LoginPage


def test_fallo_intencional(driver):
    """Falla a propósito: el usuario bloqueado nunca llega al inventario"""
    driver.get("https://saucedemo.com")
    login = LoginPage(driver)
    login.ingresar_credenciales("locked_out_user", "secret_sauce")
    login.click_login()
    assert "inventory.html" in driver.current_url