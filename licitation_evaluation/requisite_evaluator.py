import json
from licitation_evaluation.base_evaluator import BaseEvaluator

class RequisiteEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__()
        self.instructions = ""

    def _initialize_instructions(self):
        self.instructions = """"""

    def _get_data_from_licitation(self, licitation: json) -> str:
        requisites = licitation.get("5", "")
        requisites.pop("personaNatural")
        requisites.pop("documentosPersonaNatural")

        requisites_str = "Requisitos:\n"

        for i, point in enumerate(requisites.get("personaJuridica", [])):
            requisites_str += f"{i + 1}: {point}\n"

        requisites_str += "\nRequisito de Documentos:\n"

        for i, doc in enumerate(requisites.get("documentosPersonaJuridica", [])):
            if doc:
                requisites_str += f"{i + 1}: {doc}\n" 
                
        return requisites_str

    def evaluate_licitation(self, licitation: json) -> str:
        instructions = """Eres un evaluador experto de licitaciones para una empresa. 
        Tu tarea es analizar los requisitos de la una licitación y determinar qué tanto se alinean con las capacidades y criterios de la empresa. Se te dará una lista de requisitos y documentos solicitados en la licitación.
        Debes evaluar cada requisito y entregar un PUNTAJE FINAL DE COMPATIBILIDAD del 1 - 10, siendo 1 no compatible y 10 muy compatible.


        
        """
        
        data_str = self._get_data_from_licitation(licitation)
        prompt = f"{instructions}\n\nDatos de la Licitación:\n{data_str}"

        response = self.client.responses.create(
                model=self.model,  
                instructions=instructions, 
                input=prompt,                
            )

if __name__ == "__main__":
    evaluator = RequisiteEvaluator()

    import config
    from utils.utils import load_json

    licitation_path = config.PROJECT_ROOT / "web_scraping" / "scraping_results" / "licitacion_result_188-106-LE25.json"
    licitation = load_json(licitation_path, {})

    data = evaluator._get_data_from_licitation(licitation)

    print(data)