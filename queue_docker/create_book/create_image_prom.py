from fuction_file import _mongoDB, _watson

import openai
import json

class IMAGE_PROM :
    def __init__(self, API_KEY, OPENAI_API_KEY, PROJECT_ID, MONGO_PASSWORD, unique_key) :
        self.API_KEY = API_KEY
        self.PROJECT_ID = PROJECT_ID
        self.MONGO_PASSWORD = MONGO_PASSWORD
        self.unique_key = unique_key
        openai.api_key = OPENAI_API_KEY

    def mongo_client(self, MONGO_PASSWORD) :
        client = _mongoDB.mongodb_connection(MONGO_PASSWORD)
        return client

    def create_background_prom(self, ptask) :
        ptask = ptask
        
        past_stroy_en = ptask['past_stroy_en']
        try : 
            past_stroy_en = past_stroy_en['content']
        except :
            past_stroy_en = past_stroy_en['contents']

        sys_prom = "To create an image using stablediffusion, the image prompt must be in a 'children's book illustration style.' When a sentence is received, extract the important content and create a prompt that effectively represents it as a picture book cover. Select one significant event from the sentence, analyze it, and separately add all objects, actions, emotions, the subject feeling the emotions, and the mentioned time period to the prompt. An image is created in a 'children's book illustration style' depicting the most important event from the received sentence, including all objects, actions, emotions, the subject feeling the emotions, and the mentioned time period."
        prom = f'"{past_stroy_en}",Please don\'t say anything other than the story. Keep in mind that the style of the image should be \"Children\'s Book Painting Style\", and the painting should not feel too young or too rough. The prompt must not exceed 1000 characters, and this must be observed. json pormat : {{"prompts":"prompts"}}'
        messages=[
            {"role":"system",
                "content":sys_prom},
            {"role": "user","content": prom}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        response = json.loads(bytes(response["choices"][0]["message"]["content"], encoding="utf-8").decode("utf-8"))

        return response['prompts']

    def create_prom(self, ptask) :
        ptask = ptask

        face_info = ptask['face_info']

        # face info
        gender = face_info['Gender']
        age = ptask['age']
        face_shape = face_info['FaceShape']
        eyes = face_info['Eyes']
        nose = face_info['Nose']
        mouth = face_info['Mouth']
        hair = face_info['Hair']
        skin_tone = face_info['SkinTone']
        jawline_chin = face_info['JawlineChin']
        clothing = face_info['Clothing']
        accessories = face_info['Accessories']
        background_prom = self.create_background_prom(ptask)

        # background info
        description = (
            f"charactor:{age} years old child"
            f"wearing : {clothing},"
            f"accessories:{accessories},"
            f"gender:{gender},faceShape:{face_shape}, jawlineChin:{jawline_chin},"
            f"eyes:{eyes}, nose:{nose}, "
            f"mouth:{mouth}, hair:{hair}, "
            f"skinTone:{skin_tone}, "
            f"backgound : {background_prom},"
            f"age:{age} years old"
        )
        
        return description


