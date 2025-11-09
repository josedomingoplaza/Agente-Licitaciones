import os
from licitation_filter.utils.utils import load_json, save_json
from licitation_filter.filters.licitation_prefilter import LicitationPreFilter

codes_to_register_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "licitation_filter", "data", "unregistered_codes")

codes_to_register = load_json(os.path.join(codes_to_register_path, "06102025_unregistered_codes.json"), {})

licitation_prefilter = LicitationPreFilter()

for code_str, product_name in codes_to_register.items():
    code = int(code_str)
    licitation_prefilter.register_code(code, product_name)

