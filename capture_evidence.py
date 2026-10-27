import os
import time
import json
import urllib.request
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"C:\Users\MAAIC\.gemini\antigravity-ide\brain\5016e227-5393-472f-9f96-7dc8f4b7e708"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Ancho adecuado para capturas limpias y legibles
        context = browser.new_context(viewport={'width': 1300, 'height': 850})
        page = context.new_page()

        # -------------------------------------------------------------
        # 1. SWAGGER ENDPOINTS OVERVIEW
        # -------------------------------------------------------------
        print("1. Capturando Swagger UI con todos los endpoints...")
        page.goto("http://127.0.0.1:8000/swagger/")
        page.wait_for_selector(".swagger-ui")
        time.sleep(2)
        path1 = os.path.join(OUTPUT_DIR, "evidencia_1_swagger_endpoints.png")
        page.screenshot(path=path1)
        print(f"-> Guardado: {path1}")

        # -------------------------------------------------------------
        # 2. OBTENCIÓN DEL TOKEN (POST /api/v1/auth/token/)
        # -------------------------------------------------------------
        print("2. Ejecutando y capturando POST /api/v1/auth/token/...")
        token_op = page.locator('#operations-v1-v1_auth_token_create')
        token_op.click()
        time.sleep(0.5)

        token_op.locator('.try-out__btn').click()
        time.sleep(0.3)

        textarea = token_op.locator('.body-param__text')
        textarea.fill('{\n  "email": "admin@tiendaonline.com",\n  "password": "AdminPassword123!"\n}')
        time.sleep(0.3)

        token_op.locator('.execute').click()
        time.sleep(1.5)

        # Hacer scroll directamente al bloque de respuesta para que se vea el código 200 y el JSON del token
        resp_block = token_op.locator('.live-responses-table')
        resp_block.scroll_into_view_if_needed()
        time.sleep(0.5)

        path2 = os.path.join(OUTPUT_DIR, "evidencia_2_token_response.png")
        page.screenshot(path=path2)
        print(f"-> Guardado: {path2}")

        # -------------------------------------------------------------
        # 3. CONSULTA DE DATOS PERSONALES (GET /api/v1/auth/me/)
        # -------------------------------------------------------------
        print("3. Ejecutando y capturando GET /api/v1/auth/me/...")
        # Primero iniciamos sesión con el botón Django Login para usar SessionAuthentication de Swagger
        page.goto("http://127.0.0.1:8000/admin/login/?next=/swagger/")
        page.fill('input[name="username"]', 'admin@tiendaonline.com')
        page.fill('input[name="password"]', 'AdminPassword123!')
        page.click('input[type="submit"]')
        time.sleep(1.5)

        # Ahora en Swagger, expandimos /v1/auth/me/
        page.wait_for_selector(".swagger-ui")
        time.sleep(1)
        me_op = page.locator('#operations-v1-v1_auth_me_list')
        me_op.click()
        time.sleep(0.5)

        me_op.locator('.try-out__btn').click()
        time.sleep(0.3)
        me_op.locator('.execute').click()
        time.sleep(1.5)

        me_resp = me_op.locator('.live-responses-table')
        me_resp.scroll_into_view_if_needed()
        time.sleep(0.5)

        path3 = os.path.join(OUTPUT_DIR, "evidencia_3_auth_me_response.png")
        page.screenshot(path=path3)
        print(f"-> Guardado: {path3}")

        # -------------------------------------------------------------
        # 4. DJANGO ADMIN: MODELO DE USUARIO CON CAMPO 'TELEFONO'
        # -------------------------------------------------------------
        print("4. Capturando Django Admin con el campo 'telefono'...")
        page.goto("http://127.0.0.1:8000/admin/users/user/2/change/")
        time.sleep(1)
        path_admin = os.path.join(OUTPUT_DIR, "evidencia_admin_user_telefono.png")
        page.screenshot(path=path_admin)
        print(f"-> Guardado: {path_admin}")

        browser.close()

if __name__ == "__main__":
    run()
