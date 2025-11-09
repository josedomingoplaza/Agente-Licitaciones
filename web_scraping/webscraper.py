import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, data_blueprint):
        self.data_blueprint = data_blueprint
        self.soup = None

    def fetch(self, codigo_externo):
        response = requests.get(f"http://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion={codigo_externo}")
        self.soup = BeautifulSoup(response.text, "html.parser")

    def get_text_by_id(self, id_):
        tag = self.soup.find(id=id_)
        return tag.get_text(strip=True) if tag else None

    def get_by_id_or_list(self, value):
        if isinstance(value, list):
            return [self.get_text_by_id(v) for v in value]
        elif isinstance(value, dict):
            return {k: self.get_by_id_or_list(v) for k, v in value.items()}
        else:
            return self.get_text_by_id(value)

    def scrape(self, codigo_externo):
        if self.soup is None:
            self.fetch(codigo_externo)
        output = {}
        for section, content in self.data_blueprint.items():
            output[section] = self.get_by_id_or_list(content)
        return output
    
