import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 1. Configuración del Driver
driver = webdriver.Chrome()

# Espera máxima de 10 segundos
wait = WebDriverWait(driver, 10)

try:
    # --- CASO 1: Login Seguro ---
    driver.get("https://saucedemo.com")

    # Esperamos a que el campo de usuario sea visible antes de escribir
    user_input = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    user_input.send_keys("standard_user")

    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    

    # --- CASO 2: Agregar al Carrito con Verificación de Clic ---
    # Esperamos a que el botón sea "clicable"
    btn_add = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
    btn_add.click()

    # Verificamos que el contador del carrito aparezca
    badge = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    print(f"Prueba exitosa: Carrito tiene {badge.text} producto(s).")
    

    # --- CASO 3: Validación de Error de Bloqueo ---
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    driver.get("https://saucedemo.com")

    user_input = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    user_input.send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Esperamos a que el mensaje de error sea visible
    error_container = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )
    print(f"Validación de error correcta: {error_container.text}")
   

finally:
    driver.quit()