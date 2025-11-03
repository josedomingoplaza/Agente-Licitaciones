from openai import OpenAI
import dotenv
import os
dotenv.load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI()

class IndustryEvaluator:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-4.1-nano-2025-04-14"

    def evaluate_industry(self, licitation_description: str) -> str:
        instructions = "Eres un experto en clasificación de industrias. Dada la siguiente descripción de licitación, y los proyectos anteriores que la empresa ha realizado, determina si la licitación entrante es adecuada para que la empresa la asuma. Asigna una puntuación de compatibilidad del 1 al 10, donde 1 significa 'no compatible en absoluto' y 10 significa 'perfectamente compatible'. Proporciona una breve explicación para tu puntuación."
        
        prompt = f""" Descripcion licitacion: {licitation_description}

        Evaluación:"""

        response = self.client.responses.create(
                model=self.model,  
                instructions= instructions, 
                input=prompt,                
                
                max_tokens=200,
                temperature=0.1
            )

        return response.choices[0].message.content.strip()