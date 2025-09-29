from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

FICHA_URL = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs=sKUZzSlB2r97oKPV8dKA0w=="

opts = Options()
opts.add_argument("--window-size=1200,900")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
driver.get(FICHA_URL)

wait = WebDriverWait(driver, 15)
img = wait.until(EC.presence_of_element_located((By.ID, "imgAdjuntos")))
driver.execute_script("arguments[0].click();", img)

# Esperar a que se abra la nueva pestaña/ventana
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
driver.switch_to.window(driver.window_handles[-1])

# Guardar el URL en una variable
url_adjuntos = driver.current_url
print(url_adjuntos)


import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoingit

# 1. Cargar el HTML de la página de adjuntos
resp = requests.get(url_adjuntos, headers={"User-Agent": "mp-min/1.0"})
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# 2. Buscar los links de los iconos "Ver"
links = []
for a in soup.find_all("a"):
    img = a.find("img")
    if img and "ver" in (img.get("alt", "").lower() or ""):
        links.append(urljoin(url_adjuntos, a["href"]))

print("Encontrados:", len(links), "archivos")

# 3. Descargar cada archivo
os.makedirs("adjuntos", exist_ok=True)
for i, link in enumerate(links, 1):
    r = requests.get(link, headers={"User-Agent": "mp-min/1.0"}, stream=True)
    r.raise_for_status()
    # nombre desde la cabecera
    fname = None
    cd = r.headers.get("content-disposition")
    if cd and "filename" in cd:
        import re
        m = re.search(r'filename="?([^";]+)"?', cd)
        if m:
            fname = m.group(1)
    if not fname:
        fname = f"archivo_{i}.bin"
    path = os.path.join("adjuntos", fname)
    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    print("Descargado:", path)