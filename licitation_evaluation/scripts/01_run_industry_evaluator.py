import os
import json
from licitation_evaluation.industry_evaluator import IndustryEvaluator
from licitation_filter.utils.utils import load_json, save_json

licitations_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "licitation_filter","data", "complete_licitations", "passed_filter")
results_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "licitation_evaluation", "results")

industry_evaluator = IndustryEvaluator()

for i, filename in enumerate(os.listdir(licitations_path)):
    if filename.endswith(".json"):
        file_path = os.path.join(licitations_path, filename)
        print(filename)
        licitation = load_json(file_path, {})
        print(f"Código: {licitation.get('CodigoExterno')}")
        print(f"Descripción: {licitation.get('Descripcion')}\n")
        try:
            evaluation = industry_evaluator.evaluate_industry(licitation)
            print(f"Evaluación de Industria: {evaluation}\n")
            result = {
                "CodigoExterno": licitation.get("CodigoExterno"),
                "EvaluacionIndustria": evaluation,
                "Nombre": licitation.get("Nombre"),
                "Descripcion": licitation.get("Descripcion")
                }
            save_json(os.path.join(results_path, f"{licitation.get('CodigoExterno')}_evaluation.json"), result)

        except Exception as e:
            evaluation = f"Error during evaluation: {e}"
    
        print(f"Resultado guardado en: {os.path.join(results_path, f'{licitation.get('CodigoExterno')}_evaluation.json')}\n")

