import sys
import config
from pathlib import Path
from utils.utils import load_json, save_json
from web_scraping.webscraper import WebScraper

blueprint_path = config.PROJECT_ROOT / "web_scraping" / "blueprints" / "mercado_publico.json"
blueprint = load_json(blueprint_path, {})

if len(sys.argv) > 1:
    codigo_externo = sys.argv[1]
else:
    print("Usage: python run_scraper.py <codigo_externo>")
    sys.exit(0)

scraper = WebScraper(blueprint)

print("Starting scrape...")
result = scraper.scrape(codigo_externo)
print("Otro")
result = scraper.scrape(codigo_externo)
print("Otro")
result = scraper.scrape(codigo_externo)
print("Otro")
result = scraper.scrape(codigo_externo)
print("Otro")
output_path = config.PROJECT_ROOT / "web_scraping" / "scraping_results" / f"licitacion_result_{codigo_externo}.json"
save_json(output_path, result)

