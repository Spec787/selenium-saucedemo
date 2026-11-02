from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración inicial
driver = webdriver.Chrome()
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)


def ejecutar_pruebas():
    try:
        # --- CASO 1: Login Exitoso ---
        print("Ejecutando Caso 1: Login...")
        driver.get("https://saucedemo.com")
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        assert "inventory.html" in driver.current_url
        print("✅ Caso 1 completado con éxito.")

        # --- CASO 2: Agregar al Carrito ---
        print("Ejecutando Caso 2: Agregar producto...")
        boton_agregar = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        boton_agregar.click()
        badge_carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        assert badge_carrito == "1"
        print("✅ Caso 2 completado con éxito.")

        # --- CASO 3: Login Fallido (Usuario Bloqueado) ---
        print("Ejecutando Caso 3: Login fallido...")
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
        driver.get("https://saucedemo.com")
        campo_usuario = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
        campo_usuario.send_keys("locked_out_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        error_msg = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        ).text
        assert "Sorry, this user has been locked out" in error_msg
        print("✅ Caso 3 completado con éxito.")

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        print(f"URL actual: {driver.current_url}")

    finally:
        driver.quit()


if __name__ == "__main__":
    ejecutar_pruebas()