from dotenv import load_dotenv

import os

def api_key_load() :
    load_dotenv()
    API_KEY = os.environ.get('API_KEY')
    
    return API_KEY

def openai_api_key_load() :
    load_dotenv()
    API_KEY = os.environ.get('OPENAI_API_KEY')
    
    return API_KEY

def project_id_load() :
    load_dotenv()
    PROJECT_ID = os.environ.get('PROJECT_ID')
    
    return PROJECT_ID

def mongodb_password() :
    load_dotenv()
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    
    return MONGO_PASSWORD

def stability_key() :
    load_dotenv()
    STABILITY_KEY = os.environ.get('STABILITY_KEY')
    
    return STABILITY_KEY