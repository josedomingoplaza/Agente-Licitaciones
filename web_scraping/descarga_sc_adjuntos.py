import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

FICHA_URL = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs=sKUZzSlB2r97oKPV8dKA0w=="

DOWNLOAD_DIR = r"C:\Users\danie\OneDrive\Escritorio\Agente Licitaciones\Agente-Licitaciones\web_scraping\adjuntosos"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

opts = Options()
opts.add_argument("--window-size=1200,900")
# opts.add_argument("--headless=new")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

try:
    driver.get(FICHA_URL)
    wait = WebDriverWait(driver, 15)

    # Abrir "Adjuntos"
    img = wait.until(EC.presence_of_element_located((By.ID, "imgAdjuntos")))
    driver.execute_script("arguments[0].click();", img)

    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    base_url = driver.current_url
    print("Adjuntos en:", base_url)

    # ---- Preparar sesión requests con cookies de Selenium
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    for c in driver.get_cookies():
        session.cookies.set(c["name"], c["value"], domain=c.get("domain"))

    def get_hidden_fields():
        """Extrae los hidden fields ASP.NET del HTML actual."""
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        def get_value(name):
            inp = soup.find("input", {"name": name})
            return inp.get("value") if inp else ""

        return {
            "__VIEWSTATE": get_value("__VIEWSTATE"),
            "__VIEWSTATEGENERATOR": get_value("__VIEWSTATEGENERATOR"),
            "__EVENTVALIDATION": get_value("__EVENTVALIDATION"),
        }

    # ---- Encontrar los botones "Ver"
    ver_btns = driver.find_elements(By.XPATH, "//input[@type='image' and contains(@id,'_search')]")
    print("Botones Ver:", len(ver_btns))

    total = 0
    for idx, btn in enumerate(ver_btns, start=1):
        try:
            row = btn.find_element(By.XPATH, "./ancestor::tr[1]")
        except Exception:
            continue

        nombre_row = (row.text or "").strip().lower()

        # ⚠️ Filtro: solo filas que mencionen pdf/docx
        if not (".pdf" in nombre_row or ".docx" in nombre_row):
            print(f"[{idx}] Saltando (no pdf/docx): {nombre_row}")
            continue

        btn_name = btn.get_attribute("name") or btn.get_attribute("id")
        if not btn_name:
            print(f"[{idx}] Saltando (sin name/id detectable)")
            continue

        hidden = get_hidden_fields()
        payload = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": hidden["__VIEWSTATE"],
            "__VIEWSTATEGENERATOR": hidden["__VIEWSTATEGENERATOR"],
            "__EVENTVALIDATION": hidden["__EVENTVALIDATION"],
            f"{btn_name}.x": "10",
            f"{btn_name}.y": "10",
        }

        try:
            r = session.post(base_url, data=payload, timeout=90, allow_redirects=True)
        except requests.RequestException as e:
            print(f"[{idx}] Error POST: {e}")
            continue

        dispo = r.headers.get("Content-Disposition", "")
        filename = None
        if "filename=" in dispo:
            filename = dispo.split("filename=")[-1].strip().strip('"').strip("'")

        if not filename:
            if ".pdf" in nombre_row:
                filename = f"adjunto_{idx}.pdf"
            elif ".docx" in nombre_row:
                filename = f"adjunto_{idx}.docx"
            else:
                print(f"[{idx}] Saltando (no pdf/docx reconocido en nombre ni cabecera)")
                continue

        # ⚠️ Solo guardamos pdf/docx
        if not (filename.lower().endswith(".pdf") or filename.lower().endswith(".docx")):
            print(f"[{idx}] Saltando (no pdf/docx): {filename}")
            continue

        safe_name = "".join(c for c in filename if c not in r'<>:\"/\\|?*').strip()
        file_path = os.path.join(DOWNLOAD_DIR, safe_name)

        try:
            with open(file_path, "wb") as f:
                f.write(r.content)
            total += 1
            print(f"[{idx}] Descargado: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"[{idx}] Error guardando {filename}: {e}")

    print(f"✅ Descargas listas ({total} archivos) en: {DOWNLOAD_DIR}")

finally:
    driver.quit()
