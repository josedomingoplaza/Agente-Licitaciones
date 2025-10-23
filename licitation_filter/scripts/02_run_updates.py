import os
import json
import time
from datetime import datetime
from web_scraping.mercado_publico_client import MercadoPublicoClient

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def run_ai_re_analysis(full_licitation_data):
    # Placeholder for future agentic re-analysis
    pass

# --- Paths ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_root, "data", "complete_licitaciones")
state_dir = os.path.join(project_root, "state")
logs_dir = os.path.join(project_root, "logs", "update_runs")

worthy_path = os.path.join(state_dir, "tracked_worthy_licitations.json")

client = MercadoPublicoClient()
now = datetime.now()
formatted_date = now.strftime("%d%m%Y")

# 1. Fetch all active licitations
all_active_licitations = client.get_licitations_all_active()

# 2. Load worthy list
worthy_dict = load_json(worthy_path, {})

# 3. Compare for updates
updated_ids = []
update_log = []

active_lookup = {lic.get("CodigoExterno"): lic for lic in all_active_licitations}

for codigo_externo, tracked in worthy_dict.items():
    active_lic = active_lookup.get(codigo_externo)
    if not active_lic:
        continue
    fecha_cierre = active_lic.get("FechaCierre")
    codigo_estado = active_lic.get("CodigoEstado")
    if fecha_cierre != tracked.get("FechaCierre") or codigo_estado != tracked.get("CodigoEstado"):
        updated_ids.append(codigo_externo)
        update_log.append({
            "id": codigo_externo,
            "old_fecha_cierre": tracked.get("FechaCierre"),
            "new_fecha_cierre": fecha_cierre,
            "old_codigo_estado": tracked.get("CodigoEstado"),
            "new_codigo_estado": codigo_estado,
        })

# 4. Fetch updated data and save
for codigo_externo in updated_ids:
    lic_data = client.get_licitation_by_code(codigo_externo)
    if lic_data:
        save_json(os.path.join(data_dir, f"{codigo_externo}.json"), lic_data)
        run_ai_re_analysis(lic_data)
        # Update state
        worthy_dict[codigo_externo]["FechaCierre"] = lic_data.get("FechaCierre")
        worthy_dict[codigo_externo]["CodigoEstado"] = lic_data.get("CodigoEstado")
        time.sleep(2)

# 5. Log the run
summary = {
    "date": formatted_date,
    "checked": len(worthy_dict),
    "updated": len(updated_ids),
    "update_log": update_log,
}
save_json(os.path.join(logs_dir, f"{formatted_date}.json"), summary)

# 6. Save updated worthy state
save_json(worthy_path, worthy_dict)

print(f"Update run complete. {len(updated_ids)} licitations updated.")