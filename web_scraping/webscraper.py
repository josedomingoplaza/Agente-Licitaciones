import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, data_blueprint):
        self.data_blueprint = data_blueprint

    def fetch(self, codigo_externo):
        response = requests.get(f"http://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion={codigo_externo}")
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_text_by_id(self, soup, id_):
        tag = soup.find(id=id_)
        return tag.get_text(strip=True) if tag else None

    def get_by_id_or_list(self, soup, value):
        if isinstance(value, list):
            return [self.get_text_by_id(soup, v) for v in value]
        elif isinstance(value, dict):
            return {k: self.get_by_id_or_list(soup, v) for k, v in value.items()}
        else:
            return self.get_text_by_id(soup, value)

    def scrape(self, codigo_externo):
        soup = self.fetch(codigo_externo)
        output = {}
        for section, content in self.data_blueprint.items():
            output[section] = self.get_by_id_or_list(soup, content)
        return output
    
if __name__ == "__main__":
    import config
    from utils.utils import load_json

    blueprint_path = config.PROJECT_ROOT / "web_scraping" / "blueprints" / "mercado_publico.json"
    blueprint = load_json(blueprint_path, {})

    scraper = WebScraper(blueprint)
    data = scraper.scrape("1943-37-LE25")
    print(data)