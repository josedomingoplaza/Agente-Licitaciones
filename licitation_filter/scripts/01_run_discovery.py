import os
import json
import time
from tqdm import tqdm
from datetime import datetime
from web_scraping.mercado_publico_client import MercadoPublicoClient, Estado

# --- Helper Functions ---
def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def UNSPC_filter(valid_codes, licitation):
    product_codes = set()
    
    items_data = licitation.get("Items", {})
    item_list = items_data.get("Listado", [])

    for item in item_list:
        code = item.get("CodigoProducto")
        if code:
            product_codes.add(code)
  
    for code in product_codes:
        if code in valid_codes:
            return True
    
    return False

def check_is_code_registered(licitation, all_codes):
    product_codes = set()

    items_data = licitation.get("Items", {})
    item_list = items_data.get("Listado", [])
    
    for item in item_list:
        code = item.get("CodigoProducto")
        if code:
            product_codes.add(code)
  
    for code in product_codes:
        if code in all_codes:
            return True
    
    return False

def check_licitation_is_valid(licitation):
    try:
        items_data = licitation.get("CodigoExterno")
    except Exception as e:
        print(f"Error accessing licitation data: {e}")
        return False
    return True
    
# --- Paths ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_root, "data", "complete_licitaciones")
state_dir = os.path.join(project_root, "state")
logs_dir = os.path.join(project_root, "logs", "discovery_runs")
reference_dir = os.path.join(project_root, "reference")

valid_unspc_codes_path = os.path.join(reference_dir, "valid_unspc_codes.json")
all_unspc_codes_path = os.path.join(reference_dir, "all_unspc_codes.json")
discovered_ids_path = os.path.join(state_dir, "discovered_ids_history.json")

# --- Main Logic ---
client = MercadoPublicoClient()
now = datetime.now()
formatted_date = now.strftime("%d%m%Y")
formatted_time = now.strftime("%H%M%S")

# 1. Fetch today's licitations
licitations_today = client.get_licitations_for_day(formatted_date, estado=Estado.PUBLICADA)

# 2. Load discovered IDs history
discovered_ids = set(load_json(discovered_ids_path, []))

# 3. Find new items
new_licitations = [lic for lic in licitations_today if lic.get("CodigoExterno") not in discovered_ids]

# 4. Pre-filtering
valid_unspc_codes = set(load_json(valid_unspc_codes_path, []))
passed_filter_ids = []
filter_log = []

with open(all_unspc_codes_path, "r", encoding="utf-8") as f:
    codes_list = json.load(f)
all_unspc_codes = set(codes_list)

passed_count = 0
invalid_count = 0
failed_count = 0
unregistered_count = 0

invalid_licitations = []
time.sleep(2)  # To avoid hitting API limits
print(f"Beginning pre-filtering of {len(new_licitations)} new licitations...")
with tqdm(total=len(new_licitations), desc="Processing licitations") as pbar:
    for lic in new_licitations:
        codigo_externo = lic.get("CodigoExterno")
        # Try to get UNSPSC code from first item
        codigo_producto = None
        try:
            codigo_producto = lic.get("Items", {}).get("Listado", [{}])[0].get("CodigoProducto")
        except Exception:
            pass

        reason = ""
        passed = False

        tried_again = False
        while True:
            try:
                full_licitation = client.get_licitation_by_code(codigo_externo)
            except Exception as e:
                print(f"Error fetching full licitation {codigo_externo}: {e}")
                if tried_again == False:
                    print(f"Retrying once for {codigo_externo}...")
                    tried_again = True
                    time.sleep(2)
                    continue
                else:
                    print("Failed to fetch licitation after retry.")
                    full_licitation = None
                    break
            break


        if not check_licitation_is_valid(full_licitation):
            print(f"API returned faulty licitation:{codigo_externo}")
            invalid_licitations.append(codigo_externo)
            invalid_count += 1
            continue

        if UNSPC_filter(valid_unspc_codes, full_licitation):
            reason = "UNSPSC code match"
            passed_filter_ids.append(codigo_externo)
            save_json(os.path.join(data_dir, "passed_filter", f"{codigo_externo}.json"), full_licitation)
            passed = True
            passed_count += 1

        elif not check_is_code_registered(full_licitation, all_unspc_codes):
            save_json(os.path.join(data_dir, "not_registered_code_filter", f"{codigo_externo}.json"), full_licitation)
            reason = "UNSPSC code not registered"
            unregistered_count += 1

        else:
            reason = "No matching UNSPSC code"
            passed = False
            failed_count += 1
            

        filter_log.append({"id": codigo_externo, "passed": passed, "reason": reason})
        pbar.set_postfix({
            "Passed": passed_count,
            "Invalid": invalid_count,
            "Failed": failed_count,
            "Unregistered": unregistered_count
        })
        pbar.update(1)
        time.sleep(2)  # To avoid hitting API limits

print(f"Invalid licitations: {invalid_licitations}")


# 6. Log the run
summary = {
    "date": formatted_date,
    "total_found": len(licitations_today),
    "new_licitations": len(new_licitations),
    "passed_filter": len(passed_filter_ids),
    "filter_log": filter_log,
}
save_json(os.path.join(logs_dir, f"{formatted_date}_{formatted_time}.json"), summary)

# 7. Update discovered IDs history
all_ids = discovered_ids.union(set([lic.get("CodigoExterno") for lic in licitations_today]))
save_json(discovered_ids_path, list(all_ids))

print("\nDiscovery Run Summary:")
print(f"Processed {len(new_licitations)} new licitations.")
print(f"Passed pre-filter: {len(passed_filter_ids)} licitations.")
