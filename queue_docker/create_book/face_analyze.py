from fuction_file import _log_write

import openai
import base64
import json

class FACE_ANALYZE :
    def __init__(self, task, API_KEY) :
        self.API_KEY = API_KEY
        self.unique_key = task['key']
        openai.api_key = self.API_KEY

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    def analyze_image(self, image) :
        with open('create_book/prompts/image_prompt.txt', 'r') as f :
            load_system_promt = f.read()
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": load_system_promt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}"
                        }
                    }
                ]
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=2000,  # Adjust token count based on your requirements
            response_format={ "type": "json_object" }
        )

        analyzed_image_json = response['choices'][0]['message']['content']

        return analyzed_image_json

    def create_analyzed_improm(self) :
        image_path = f'../upload_images/{self.unique_key}.png'
        encode_image = self.encode_image(image_path)

        analyzed_image_json = self.analyze_image(encode_image)

        return json.loads(analyzed_image_json)