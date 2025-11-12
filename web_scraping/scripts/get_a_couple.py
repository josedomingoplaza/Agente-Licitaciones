import config
import os
from pathlib import Path
from utils.utils import load_json, save_json
from web_scraping.webscraper import WebScraper
import time

blueprint_path = config.PROJECT_ROOT / "web_scraping" / "blueprints" / "mercado_publico.json"
licitations_directory = config.PROJECT_ROOT / "licitation_filter" / "data" / "complete_licitations" / "no_registered_codes"
results_directory = config.PROJECT_ROOT / "web_scraping" / "scraping_results"
blueprint = load_json(blueprint_path, {})

codes = []

for i, filename in enumerate(os.listdir(licitations_directory)):
    if i >= 10:
        break
    if filename.endswith(".json"):
        codes.append(filename.replace(".json", ""))




scraper = WebScraper(blueprint)

print("Starting scrape...")
for codigo_externo in codes:
    result = scraper.scrape(codigo_externo)
    save_json(results_directory / f"licitacion_result_{codigo_externo}.json", result)
    time.sleep(2)  # Small delay between requests to avoid overwhelming the server

