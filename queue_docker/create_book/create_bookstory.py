from fuction_file import _log_write, _mongoDB, _watson
from deep_translator import GoogleTranslator

import openai
import json

class CREATE_STORY :
    def __init__(self, API_KEY, OPENAI_API_KEY, PROJECT_ID, MONGO_PASSWORD, task) :
        self.task = task
        self.API_KEY = API_KEY
        self.PROJECT_ID = PROJECT_ID
        self.MONGO_PASSWORD = MONGO_PASSWORD
        openai.api_key = OPENAI_API_KEY

    def mongo_client(self, MONGO_PASSWORD) :
        client = _mongoDB.mongodb_connection(MONGO_PASSWORD)
        db = client['cbook']
        return db
    
    def use_watsonx(self, prompts, sys_prompt) :
        model_name = "meta-llama/llama-3-70b-instruct" #'mistralai/mistral-large' ModelTypes.LLAMA_3_70B_INSTRUCT.value # ModelTypes.LLAMA_2_70B_CHAT.value
        decoding_method = "sample"
        max_new_tokens = 4096
        min_new_tokens = 1
        temperature = 1.0
        repetition_penalty = 1.0
        results = _watson.use_watson(
                    self.API_KEY,
                    self.PROJECT_ID,
                    prompts,
                    model_name,
                    decoding_method,
                    sys_prompt,
                    max_new_tokens,
                    min_new_tokens,
                    temperature,
                    repetition_penalty
                )
        return results
    
    def translater(self, stroy) :
        sys_prom = (
            "Your role is to translate children's books in English into Korean\\n"+
            "You have to use easy vocabulary to make it easier for kids to understand and translate it thickly\\n"+
            "Leave the {{name}} part as it is.\\n"+
            "When translating options (ex: options:A.content, B.content, C.content), translate them as selectable options in a suitable manner.\\n"+
            "Output example:\\n"+
            "json\\n"+
            "{'trans':'content'}\\n"+
            "")
        prom = stroy
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

        return json.loads(response['choices'][0]['message']['content'])

    def trans_result(self, preprocessed_result) :
        kr_story = {}
        
        try :
            story_title = preprocessed_result['titles'] 
        except :
            story_title = preprocessed_result['title'] 

        story_contents = preprocessed_result['content']
        story_options = preprocessed_result['options']

        kr_title = self.translater(story_title)['trans']

        kr_contents = []
        for story in story_contents :
            try:
                if story:  # 스토리가 None이거나 빈 값이 아닌지 확인
                    eng_story = self.translater(story)['trans']
                else:
                    eng_story = ''
                kr_contents.append(eng_story)
            except Exception as e:
                _log_write.write_log(500, f"Error translating story: Error: {e}")
                kr_contents.append('')  # 빈 문자열 또는 기본 오류 메시지를 추가

        kr_options = []
        for story in story_options :
            try:
                if story:  # 스토리가 None이거나 빈 값이 아닌지 확인
                    eng_story = self.translater(story)['trans']
                else:
                    eng_story = ''
                kr_options.append(eng_story)
            except Exception as e:
                _log_write.write_log(500, f"Error translating story: Error: {e}")
                kr_options.append('')  # 빈 문자열 또는 기본 오류 메시지를 추가

        kr_story['title'] = kr_title
        kr_story['contents'] = kr_contents
        kr_story['options'] = kr_options

        return kr_story
    
    def create_book(self) :
        age = self.task['age']
        sex = self.task['sex']
        theme = self.task['thema']
        favorite = self.task['favorite']
        teach = self.task['teach']
        
        prompt = f"Children's bookmaking info: {{Name: {{name}}, Age: {age}, Gender: {sex}, Subject: {theme}, Favorite: {favorite}, Teaching: {teach}}} use this info when you make book"
        with open('create_book/prompts/story.txt', 'r', encoding='UTF-8') as f:
            sys_prompt = f.read()
        
        results = self.use_watsonx(prompt, sys_prompt)
        kr_story = self.trans_result(results)
        
        return results, kr_story