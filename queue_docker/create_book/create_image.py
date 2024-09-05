import requests
import os

def create_image(stability_key, unique_key, prompt) :
    FILE_PATH = 'stroy_images/'
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/control/style",
        headers={
            "authorization": f"Bearer {stability_key}",
            "accept": "image/*"
        },
        files={
            "image": open("create_book/source_image/source.png", "rb")
        },
        data={
            "prompt": prompt,
            "output_format": "webp"
        },
    )

    files_in_directory = os.listdir(FILE_PATH)
    # 주어진 이름과 동일한 이름을 가진 이미지 파일 찾기
    matching_files = [file for file in files_in_directory 
                      if os.path.splitext(file)[0].split('_')[0] == unique_key]
    
    num = len(matching_files)

    if response.status_code == 200:
        with open(f"{FILE_PATH}{unique_key}_{num}.png", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))