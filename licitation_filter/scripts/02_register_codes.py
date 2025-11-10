import config
from pathlib import Path
from licitation_filter.utils.utils import load_json
from licitation_filter.filters.licitation_prefilter import LicitationPreFilter

date_to_register = "06102025"
codes_to_register_path = config.PROJECT_ROOT / "licitation_filter" / "data" / "unregistered_codes"
codes_to_register = load_json(codes_to_register_path / f"{date_to_register}_unregistered_codes.json", {})

licitation_prefilter = LicitationPreFilter()

for code_str, product_name in codes_to_register.items():
    code = int(code_str)
    licitation_prefilter.register_code(code, product_name)

