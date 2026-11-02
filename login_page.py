from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Selectores (Locators)
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_msg = (By.CSS_SELECTOR, "[data-test='error']")

    def ingresar_credenciales(self, usuario, password):
        self.wait.until(EC.visibility_of_element_located(self.username_field)).send_keys(usuario)
        self.driver.find_element(*self.password_field).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    def obtener_error(self):
        return self.wait.until(EC.visibility_of_element_located(self.error_msg)).text
    