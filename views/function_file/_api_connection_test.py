from views.function_file import _watson, _log_write

def api_connection_test(API_KEY, PROJECT_ID) :
    sys_prompt = ''
    prompt = "how are you?"
    model_name = "meta-llama/llama-3-70b-instruct" #'mistralai/mistral-large' ModelTypes.LLAMA_3_70B_INSTRUCT.value # ModelTypes.LLAMA_2_70B_CHAT.value
    decoding_method = "sample"
    max_new_tokens = 30
    min_new_tokens = 1
    temperature = 1.0
    repetition_penalty = 1.0

    try:
        # Watson API 호출
        response = _watson.use_watson(
            API_KEY,
            PROJECT_ID,
            prompt,
            model_name,
            decoding_method,
            sys_prompt,
            max_new_tokens,
            min_new_tokens,
            temperature,
            repetition_penalty
        )
        
        if response:
            return 200
        else:
            _log_write.write_log(500, f"ServerStart(API connect) : API response was None or empty.")  # 오류 메시지 출력
            return 500
    
    except Exception as e:
        # 예외 발생 시 오류 메시지 출력
        _log_write.write_log(500, f"ServerStart(API connect) : Connection failed: {e}")
        return 500