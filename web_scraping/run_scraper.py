import json
import os
from web_scraping.webscraper import WebScraper

with open("web_scraping/blueprints/mercado_publico.json", "r", encoding="utf-8") as f:
    blueprint = json.load(f)

# codigo_externo = "1191382-16-LP25"

# scraper = WebScraper(blueprint)
# print("Starting scrape...")
# result = scraper.scrape(codigo_externo)
# print("Scrape completed.")
# print(json.dumps(result, indent=2, ensure_ascii=False))
# output_dir = "web_scraping/scraping_results"
# os.makedirs(output_dir, exist_ok=True)


# output_path = os.path.join(output_dir, "licitacion_result.json")
# with open(output_path, "w", encoding="utf-8") as f:
#     json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        codigo_externo = sys.argv[1]
    else:
        print("Usage: python run_scraper.py <codigo_externo>")
        sys.exit(0)

    scraper = WebScraper(blueprint)
    print("Starting scrape...")
    result = scraper.scrape(codigo_externo)
    print("Ningun problema papi")
    result = scraper.scrape(codigo_externo)
    print("Ningun problema papi")
    result = scraper.scrape(codigo_externo)
    print("Ningun problema papi")
    result = scraper.scrape(codigo_externo)
    print("Scrape completed.")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    output_dir = "web_scraping/scraping_results"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"licitacion_result_{codigo_externo}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)