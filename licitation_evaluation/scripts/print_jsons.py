from licitation_filter.utils.utils import load_json
import os
    
results_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "licitation_evaluation", "results")

for i, filename in enumerate(os.listdir(results_path)):
    content = load_json(os.path.join(results_path, filename), {})
    print(f"Contenido de {filename}:")
    print(f"Descripción: {content.get('Descripcion', 'No description found')}")
    print(f"Evaluación: {content.get('EvaluacionIndustria', 'No evaluation found')}")
    print("\n-----------------------\n")
