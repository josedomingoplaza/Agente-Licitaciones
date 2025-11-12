import json
from licitation_evaluation.base_evaluator import BaseEvaluator

class CriteriaEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__()

    def _get_data_from_licitation(self, licitation: json) -> str:
        criteria_data = licitation.get("6")
        criteria = "Criteria:\n"

        for key in criteria_data.keys():
            if criteria_data.get(key).get("nombre") is not None:
                criteria += f"Nombre: {criteria_data.get(key).get("nombre")}\nObservación: {criteria_data.get(key).get("observacion")}\nPonderación: {criteria_data.get(key).get("ponderacion")}\n\n"

        return criteria
    
    

    def evaluate_licitation(self, licitation: json) -> str:
        instructions = """"""
        
        data_str = self._get_data_from_licitation(licitation)
        prompt = f"{instructions}\n\nDatos de la Licitación:\n{data_str}"

        response = self.client.responses.create(
                model=self.model,  
                instructions=instructions, 
                input=prompt,                
            )

if __name__ == "__main__":
    evaluator = CriteriaEvaluator()

    import config
    from utils.utils import load_json

    licitation_path = config.PROJECT_ROOT / "web_scraping" / "scraping_results" / "licitacion_result_188-106-LE25.json"
    licitation = load_json(licitation_path, {})

    data = evaluator._get_data_from_licitation(licitation)

    

    print(type(data))