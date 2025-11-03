from licitation_filter.filters.licitation_prefilter import LicitationPreFilter
from web_scraping.mercado_publico_client import MercadoPublicoClient, Estado, Region
from licitation_filter.utils.utils import load_json, save_json
import os
import time
from tqdm import tqdm
import argparse

def run_licitation_discovery():

    parser = argparse.ArgumentParser(description="Run licitation discovery for a given date.")
    parser.add_argument("--date", type=str, default=time.strftime("%d%m%Y"), help="Date to run discovery for (ddmmyyyy)")
    args = parser.parse_args()

    # Initializing classes
    licitation_prefilter = LicitationPreFilter()
    mercado_publico_client = MercadoPublicoClient()

    # Getting date
    current_date = args.date
    current_time = time.strftime("%H%M%S")

    # File paths
    file_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    known_licitations_path = os.path.join(file_root, "state", "discovered_ids_history.json")
    unregistered_licitations_path = os.path.join(file_root, "data", "complete_licitations", "no_registered_codes")
    unregistered_codes_path = os.path.join(file_root, "data", "unregistered_codes")
    passed_licitations_path = os.path.join(file_root, "data", "complete_licitations", "passed_filter")
    log_directory = os.path.join(file_root, "logs")

    known_licitations = set(load_json(known_licitations_path, set()))
    print("---- Beginning search for valid licitations ----")
    print(f"           ----- Date: {current_date} -----\n")
    new_licitations = mercado_publico_client.get_new_licitations_for_day(current_date, known_licitations, Estado.PUBLICADA)
    print(f"Fetched {len(new_licitations)} new licitations.")
    time.sleep(2)

    passed_count = 0
    unregistered_count = 0
    failed_count = 0
    invalid_count = 0

    unregistered_products = load_json(os.path.join(unregistered_codes_path, f"{current_date}_unregistered_codes.json"), {})

    passed_licitations = []
    discovered_ids = set()
    logs = {}

    with tqdm(total=len(new_licitations), desc="Processing licitations") as pbar:
        for licitation in new_licitations:
            filter_result = ""
            codigo_externo = licitation.get("CodigoExterno")

            try:
                full_licitation = mercado_publico_client.get_licitation_by_code(codigo_externo)
            except Exception as e:
                print(f"Error fetching licitation {codigo_externo}: {e}")
                invalid_count += 1
                continue

            time.sleep(2)

            if not licitation_prefilter.licitation_has_id(full_licitation):
                print(f"Licitation {codigo_externo} is missing ID.")
                invalid_count += 1
                continue

            if licitation_prefilter.region_filter(full_licitation) == False:
                failed_count += 1
                filter_result = "Region filter failed"

            else:
                UNSPC_filter_result, unregistered_licitation_products = licitation_prefilter.UNSPC_filter(full_licitation)
                for code, name in unregistered_licitation_products.items():
                            unregistered_products[str(code)] = name
                save_json(os.path.join(unregistered_codes_path, f"{current_date}_unregistered_codes.json"), unregistered_products)

                if UNSPC_filter_result == "pass":
                    passed_count += 1
                    filter_result = "Passed"
                    passed_licitations.append(codigo_externo)
                    save_json(os.path.join(passed_licitations_path, f"{codigo_externo}.json"), full_licitation)
                
                elif UNSPC_filter_result == "unregistered":
                    unregistered_count += 1
                    filter_result = "No registered codes found"
                    save_json(os.path.join(unregistered_licitations_path, f"{codigo_externo}.json"), full_licitation)

                else:
                    failed_count += 1
                    filter_result = "UNSPSC filter failed"

            discovered_ids.add(codigo_externo)
            known_licitations.update(discovered_ids)
            save_json(known_licitations_path, list(known_licitations))


            

            log = {codigo_externo: {
                "Filter state": filter_result,
            }}
            logs.update(log)
            
            pbar.set_postfix({
                "Passed": passed_count,
                "Invalid": invalid_count,
                "Failed": failed_count,
                "Unregistered": unregistered_count
            })
            pbar.update(1)


    # Save logs
    save_json(os.path.join(log_directory, f"log_{current_date}_{current_time}.json"), logs)

    print("Processing complete.")

if __name__ == "__main__":
    run_licitation_discovery()

            

            

            
            



            












