from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración del navegador
driver = webdriver.Chrome()

def wait_for_element(by, value):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, value))
    )

try:
    # Inicio de sesión
    print("Navegando a la página de inicio de sesión...")
    driver.get("http://127.0.0.1:5000/login")
    wait_for_element(By.TAG_NAME, "form")
    print("Página de inicio de sesión cargada.")

    print("Rellenando formulario de inicio de sesión...")
    driver.find_element(By.NAME, "username").send_keys("admin1234")
    driver.find_element(By.NAME, "password").send_keys("admin1234")
    driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    print("Inicio de sesión realizado correctamente.")
    # Esperar hasta que se haya iniciado sesión

    # Buscar "Smirnoff" en el listado de productos
    print("Navegando a la página de ver productos...")
    driver.get("http://127.0.0.1:5000/productos")
    wait_for_element(By.NAME, "search")
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys("Smirnoff")
    search_box.submit()
    print("Buscando 'Smirnoff' en el listado de productos...")
    wait_for_element(By.TAG_NAME, "table")
    print("Búsqueda completada.")
    time.sleep(2)  # Espera adicional

    # Editar producto "Smirnoff"
    print("Navegando a la página de edición de producto...")
    producto_id = driver.find_element(By.XPATH, "//tr[td[contains(text(), 'Smirnoff')]]").get_attribute("data-id")
    driver.get(f"http://127.0.0.1:5000/productos/editar_producto/{producto_id}")
    wait_for_element(By.TAG_NAME, "form")
    print("Página de edición de producto cargada.")
    
    print("Editando producto 'Smirnoff'...")
    driver.find_element(By.NAME, "nombre").clear()
    driver.find_element(By.NAME, "nombre").send_keys("Smirnoff Editado")
    driver.find_element(By.NAME, "precio_u").clear()
    driver.find_element(By.NAME, "precio_u").send_keys("150")
    Select(driver.find_element(By.NAME, "fk_cat")).select_by_value("2")
    driver.find_element(By.NAME, "contenido").clear()
    driver.find_element(By.NAME, "contenido").send_keys("Contenido Editado")
    driver.find_element(By.NAME, "stock").clear()
    driver.find_element(By.NAME, "stock").send_keys("15")
    driver.find_element(By.NAME, "marca").clear()
    driver.find_element(By.NAME, "marca").send_keys("Marca Editada")
    driver.find_element(By.NAME, "cod_barras").clear()
    driver.find_element(By.NAME, "cod_barras").send_keys("1234567890124")
    edit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", edit_button)
    edit_button.click()
    print("Producto 'Smirnoff' editado correctamente.")
    time.sleep(2)  # Espera adicional

    # Eliminar producto "Smirnoff Editado"
    print("Navegando a la página de productos para eliminar producto...")
    driver.get("http://127.0.0.1:5000/productos")
    wait_for_element(By.TAG_NAME, "table")
    eliminar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//tr[td[contains(text(), 'Smirnoff Editado')]]//button[text()='Eliminar']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", eliminar_button)
    eliminar_button.click()
    WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()
    print("Producto 'Smirnoff Editado' eliminado correctamente.")
    time.sleep(2)  # Espera adicional

    # Registrar producto
    print("Navegando a la página de registrar producto...")
    driver.get("http://127.0.0.1:5000/productos/registrar_producto")
    wait_for_element(By.TAG_NAME, "form")
    print("Página de registrar producto cargada.")

    print("Rellenando formulario de nuevo producto...")
    driver.find_element(By.NAME, "nombre").send_keys("Producto Test")
    driver.find_element(By.NAME, "precio_u").send_keys("10")
    categoria_select = Select(driver.find_element(By.NAME, "fk_cat"))
    categoria_select.select_by_value("1")
    contenido_select = Select(driver.find_element(By.NAME, "contenido"))
    contenido_select.select_by_value("500ml")
    driver.find_element(By.NAME, "stock").send_keys("50")
    driver.find_element(By.NAME, "marca").send_keys("Marca Test")
    driver.find_element(By.NAME, "cod_barras").send_keys("1234567890123")

    # Hacer clic en el botón para registrar el producto
    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
    add_button.click()
    print("Producto añadido correctamente.")

except Exception as e:
    print(f"Error durante la prueba de productos: {e}")
    driver.save_screenshot("error_prueba_productos.png")

finally:
    driver.quit()
