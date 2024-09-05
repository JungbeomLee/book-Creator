from langchain_community.llms import WatsonxLLM
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods

def use_watson(API_KEY, 
               PROJECT_ID, 
               prompts:str,
               model_name:str,
               decoding_method:str,
               sys_prompt:str,
               max_new_tokens:int=100,
               min_new_tokens:int=30,
               temperature:int=1.0,
               repetition_penalty:int=1.0) :
    
    wml_credentials = {
        "apikey": API_KEY,
        "url": 'https://us-south.ml.cloud.ibm.com'
    }

    assert not any(map(lambda prompt: len(prompt) < 1, prompts)), "make sure none of the prompts in the inputs prompts are empty"

    # Instantiate parameters for text generation
    model_params = {
        GenParams.DECODING_METHOD: decoding_method,
        GenParams.MIN_NEW_TOKENS: min_new_tokens,
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.RANDOM_SEED: 2737,
        GenParams.TEMPERATURE: temperature,
        GenParams.REPETITION_PENALTY: repetition_penalty,
    }
    
    SYS_PROMPT = f"{sys_prompt}"
    SYS_TAG_START = "<<SYS>>"
    SYS_TAG_END = "<</SYS>>"
    INST_TAG_START = "<<INST>>"
    INST_TAG_END = "<</INST>>"
    USER_INQUERY = f"{prompts}"

    if model_params[GenParams.DECODING_METHOD].find("llama") != -1 :
        QUERY = f"{SYS_TAG_START}{SYS_PROMPT}{SYS_TAG_END}\n\n{INST_TAG_START} 사용자 질문 : {USER_INQUERY} 답변: {INST_TAG_END}"
    else:
        QUERY = f"{SYS_PROMPT}\n\n사용자 질문 : {USER_INQUERY} 답변:"

    # Instantiate a model proxy object to send your requests
    model = Model(
        model_id=model_name, #'mistralai/mistral-large' ModelTypes.LLAMA_3_70B_INSTRUCT.value # ModelTypes.LLAMA_2_70B_CHAT.value
        params=model_params,
        credentials=wml_credentials,
        project_id=PROJECT_ID)

    response = model.generate_text(prompt = QUERY)

    return response