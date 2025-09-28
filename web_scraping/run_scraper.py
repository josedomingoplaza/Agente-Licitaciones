import json
import os
from webscraper import WebScraper

with open("web_scraping/blueprints/mercado_publico.json", "r", encoding="utf-8") as f:
    blueprint = json.load(f)

url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs=cR1K+HlJLrGk9PeP2HSzsQ=="

scraper = WebScraper(url, blueprint)
result = scraper.scrape()

output_dir = "web_scraping/scraping_results"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "licitacion_result.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)