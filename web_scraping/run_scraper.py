import json
import os
from web_scraping.webscraper import WebScraper

with open("web_scraping/blueprints/mercado_publico.json", "r", encoding="utf-8") as f:
    blueprint = json.load(f)

url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs=Vd+8jLS/0CmpmYxy4OF9tQ=="

scraper = WebScraper(url, blueprint)
print("Starting scrape...")
result = scraper.scrape()
print("Scrape completed.")
print(json.dumps(result, indent=2, ensure_ascii=False))
output_dir = "web_scraping/scraping_results"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "licitacion_result.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)