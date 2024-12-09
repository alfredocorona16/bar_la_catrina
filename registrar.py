from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Configuración del navegador
driver = webdriver.Edge()

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


    # Registrar producto
    print("Navegando a la página de registrar producto...")
    driver.get("http://127.0.0.1:5000/productos/registrar_producto")
    wait_for_element(By.TAG_NAME, "form")
    print("Página de registrar producto cargada.")

    print("Rellenando formulario de nuevo producto...")
    driver.find_element(By.NAME, "nombre").send_keys("Producto Test")
    driver.find_element(By.NAME, "precio_u").send_keys("10")

    # Imprimir opciones disponibles en fk_cat
    categoria_select = Select(driver.find_element(By.NAME, "fk_cat"))
    opciones_categoria = [option.get_attribute("value") for option in categoria_select.options]
    print(f"Opciones disponibles en fk_cat: {opciones_categoria}")
    categoria_select.select_by_value("1")

    # Imprimir opciones disponibles en contenido
    contenido_select = Select(driver.find_element(By.NAME, "contenido"))
    opciones_contenido = [option.get_attribute("value") for option in contenido_select.options]
    print(f"Opciones disponibles en contenido: {opciones_contenido}")
    # Selecciona una opción válida de las disponibles
    contenido_select.select_by_value("500ml")

    driver.find_element(By.NAME, "stock").send_keys("500ml")
    driver.find_element(By.NAME, "marca").send_keys("Marca Test")
    driver.find_element(By.NAME, "cod_barras").send_keys("1234567890123")

    try:
        # Esperar a que el botón sea clicable
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary"))
        )

        # Desplazar la vista hacia el botón
        driver.execute_script("arguments[0].scrollIntoView(true);", button)

        # Hacer clic en el botón
        button.click()
        print("Producto añadido correctamente.")
        
        # Esperar a que el modal aparezca y luego desaparezca
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "modal-id")))
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "modal-id")))

    except Exception as e:
        print(f"No se pudo hacer clic en el botón de registrar producto: {e}")
        driver.save_screenshot("error_registrar_producto.png")

except Exception as e:
    print(f"Error durante la prueba de registrar producto: {e}")
    driver.save_screenshot("error_registrar_producto.png")

finally:
    driver.quit()
