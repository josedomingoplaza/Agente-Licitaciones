import json
import os
from licitation_filter.utils.utils import load_json, save_json
from web_scraping.mercado_publico_client import MercadoPublicoClient, Region

class LicitationPreFilter:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        valid_codes_path = os.path.join(script_dir, "../reference/all_unspc_codes.json")
        all_codes_path = os.path.join(script_dir, "../reference/all_unspc_codes.json")

        self.valid_codes = set()
        self.all_codes = set()
        self._load_valid_codes(valid_codes_path)
        self._load_all_codes(all_codes_path)
        self.prohibited_regions = [Region.MAGALLANES, Region.LOS_LAGOS, Region.COQUIMBO]

    def _load_valid_codes(self, codes_path):
        if os.path.exists(codes_path):
            self.valid_codes = load_json(codes_path, set())
        else:
            print(f"Warning: Codes file {codes_path} does not exist.")

    def _load_all_codes(self, all_codes_path):
        if os.path.exists(all_codes_path):
            self.all_codes = load_json(all_codes_path, set())
        else:
            print(f"Warning: All codes file {all_codes_path} does not exist.")

    def get_licitation_product_codes(self, licitation):
        product_codes = set()
        
        items_data = licitation.get("Items", {})
        item_list = items_data.get("Listado", [])

        for item in item_list:
            code = item.get("CodigoProducto")
            if code:
                product_codes.add(code)

        return product_codes
    
    def licitation_has_id(self, licitation):
        try:
            _ = licitation.get("CodigoExterno")
        except Exception as e:
            print(f"Error accessing licitation data: {e}")
            return False
        return True
    
    def UNSPC_filter(self, licitation):
        unregistered_products = {}
        passed_filter = False
        licitation_is_registered = False
        
        items_data = licitation.get("Items", {})
        item_list = items_data.get("Listado", [])

        for item in item_list:
            code = item.get("CodigoProducto")
            name = item.get("NombreProducto")

            if code in self.all_codes:
                licitation_is_registered = True
                if code in self.valid_codes:
                    passed_filter = True
            else:
                unregistered_products[code] = name

        if passed_filter:
            return "pass", unregistered_products    
          
        elif not licitation_is_registered:
            return "unregistered", unregistered_products
        
        else:
            return "fail", unregistered_products
        
    def region_filter(self, licitation):
        comprador = licitation.get("Comprador", {})
        region = comprador.get("RegionUnidad")
        if region in self.prohibited_regions:
            return False
        return True

    
if __name__ == "__main__":


    licitation_prefilter = LicitationPreFilter()

    all_codes = licitation_prefilter.all_codes
    valid_codes = licitation_prefilter.valid_codes
    for a in valid_codes:
        print(a)


    # print(len(all_codes))
    # print(len(valid_codes))
    # example_licitation_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/complete_licitations/passed_filter/557954-4-L125.json")

    # example_licitation = load_json(example_licitation_path, {})

    # filter_result, unregistered_products = licitation_prefilter.UNSPC_filter(example_licitation)

    # prohibited_regions = [Region.ANTOFAGASTA, Region.ATACAMA, Region.COQUIMBO, Region.METROPOLITANA]

    # if not licitation_prefilter.region_filter(example_licitation, prohibited_regions):
    #     print("Licitation is from a prohibited region.")
    # else:
    #     print("Licitation is from an allowed region.")

    # print("Filter result:", filter_result)
    # print("Unregistered products:", unregistered_products)