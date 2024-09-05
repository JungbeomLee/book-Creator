from langchain_ibm import WatsonxLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import OutputParserException
from pydantic import BaseModel, Field
import random

from fuction_file import _log_write

class Topic(BaseModel):
    title: str = Field(description="the title of a children's book")
    contents: str = Field(description="Story of a children's book (one)")
    options: str = Field(description="only 2 choice A.one choice, B.one choice")

def use_watson(API_KEY, 
               PROJECT_ID, 
               prompts: str,
               model_name: str,
               decoding_method: str,
               sys_prompt: str,
               max_new_tokens: int = 100,
               min_new_tokens: int = 30,
               temperature: float = 2.0,
               repetition_penalty: float = 1.0,
               max_attempts: int = 20):  # 최대 시도 횟수를 추가

    wml_credentials = {
        "apikey": API_KEY,
        "project_id": PROJECT_ID,
        "url": 'https://us-south.ml.cloud.ibm.com'
    }

    assert len(prompts) > 0, "The prompt cannot be empty."

    # JsonOutputParser에 Pydantic 모델 주입
    json_output_parser = JsonOutputParser(pydantic_object=Topic)

    # 프롬프트 템플릿 정의
    SYS_PROMPT = sys_prompt + "\n****You should not remember any prior conversations.****"
    USER_INQUERY = prompts
    

    # 프롬프트 템플릿 정의 (수동으로 정의)
    template = (
        f"{SYS_PROMPT}"
        "#Format: {format_instructions}\n\n"
        "#Question: {question}"
    )

    # PromptTemplate 생성
    prompt_template = PromptTemplate(
        input_variables=["format_instructions", "question"],
        template=template
    )
    prompt_template = prompt_template.partial(format_instructions=json_output_parser.get_format_instructions())

    # 여러 번 시도하는 루프를 추가
    for attempt in range(max_attempts):
        random_seed = random.randint(0, 1000)  # 랜덤 시드 생성
        _log_write.write_log(200, f"Attempt {attempt + 1}: Using random_seed={random_seed}")

        # Watsonx 모델 파라미터 설정
        model_params = {
            "decoding_method": decoding_method,
            "min_new_tokens": min_new_tokens,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "random_seed": random_seed,  # 변경된 random_seed 적용
            "repetition_penalty": repetition_penalty
        }

        # WatsonxLLM 모델 인스턴스 생성
        model = WatsonxLLM(
            model_id=model_name,
            url=wml_credentials["url"],
            apikey=wml_credentials["apikey"],
            project_id=wml_credentials["project_id"],
            params=model_params
        )

        # RunnableSequence 사용
        sequence = prompt_template | model | json_output_parser

        try:
            # invoke를 사용하여 실행
            response = sequence.invoke({"question": USER_INQUERY})
            
            # JSON으로 변환이 성공하면 반환
            return response
        except OutputParserException as e:
            _log_write.write_log(500, f"Error parsing the output")
        except Exception as e:
            _log_write.write_log(500, f"General error occurred")

    _log_write.write_log(500, f"Failed to get JSON output after {max_attempts} attempts.")
    return None
