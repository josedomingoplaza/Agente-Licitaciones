import requests
import os
from enum import Enum
import time
import json
from dotenv import load_dotenv
load_dotenv()


BASE_URL = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
TICKET = os.getenv("MERCADO_PUBLICO_API_KEY")

class Estado(str, Enum):
    PUBLICADA = "publicada"
    CERRADA = "cerrada"
    DESIERTA = "desierta"
    ADJUDICADA = "adjudicada"
    REVOCADA = "revocada"
    SUSPENDIDA = "suspendida"
    ACTIVAS = "activas"

class Region(str, Enum):
    ARICA_Y_PARINACOTA = "Región de Arica y Parinacota"
    TARAPACA = "Región de Tarapacá"
    ANTOFAGASTA = "Región de Antofagasta"
    ATACAMA = "Región de Atacama"
    COQUIMBO = "Región de Coquimbo"
    VALPARAISO = "Región de Valparaíso"
    METROPOLITANA = "Región Metropolitana de Santiago"
    O_HIGGINS = "Región del Libertador General Bernardo O'Higgins"
    MAULE = "Región del Maule"
    ÑUBLE = "Región de Ñuble"
    BIOBIO = "Región del Biobío"
    ARAUCANIA = "Región de La Araucanía"
    LOS_RIOS = "Región de Los Ríos"
    LOS_LAGOS = "Región de Los Lagos"
    AYSEN = "Región de Aysén del General Carlos Ibáñez del Campo"
    MAGALLANES = "Región de Magallanes y de la Antártica Chilena"

class MercadoPublicoClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or TICKET
        self.base_url = BASE_URL

    def get_licitations_for_day(self, date: str, estado: Enum = None):
        params = {
            "fecha": date,
            "ticket": self.api_key
        }
        if estado:
            if not isinstance(estado, Estado):
                raise ValueError(f"estado must be an instance of Estado enum, got {estado}")
            params["estado"] = estado.value
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json().get("Listado", [])
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
        
    def get_licitation_codes_for_day(self, date: str, estado: Enum = None):
        licitations = self.get_licitations_for_day(date, estado)
        return [lic["CodigoExterno"] for lic in licitations if "CodigoExterno" in lic]
    
    def get_licitation_by_code(self, code: str):
        params = {
            "codigo": code,
            "ticket": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            licitations = response.json().get("Listado", [])
            if licitations:
                return licitations[0]
            else:
                print(f"No licitation found with code: {code}")
                return None
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def filter_licitations_by_regions(self, licitations: list, prohibited_regions: list):
        if not isinstance(prohibited_regions, list):
            raise ValueError(f"prohibited_regions must be a list, got {prohibited_regions}")
        filtered = []
        for lic in licitations:
            comprador = lic.get("Comprador", {})
            region = comprador.get("RegionUnidad")
            if region not in prohibited_regions:
                filtered.append(lic)
        return filtered
    
    def get_new_licitations_for_day(self, date: str, known_codes: set, estado: Enum = None):
        licitations = self.get_licitations_for_day(date, estado)
        new_licitations = [lic for lic in licitations if lic.get("CodigoExterno") not in known_codes]
        return new_licitations

if __name__ == "__main__":
    import json
    client = MercadoPublicoClient()
    date = "10102025"  # ddmmaaaa
    
    print(client.get_licitations_for_day(date, Estado.PUBLICADA))



