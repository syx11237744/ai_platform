import os
import requests
import json

def image_generate(content: str):
    url = 'http://localhost:8080/v1/images/generations/'
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    generate = {
        "prompt": content,
        "size": '256x256',
    }
    # print(json.dumps(generate))
    data_json = json.dumps(generate)
    response = requests.post(url, headers=header, data=data_json)
    # print(response.status_code) # code = 500
    if response.status_code == 200:
        # 定义保存路径并保存
        # print(response.json()['data'][0]['url'])
        return response.json()['data'][0]['url']
    else:
        # 错误输出
        return f"Please say \"Failed to generate figure: {response.status_code} {response.text}\""

if __name__ == "__main__":
    url = image_generate('floating hair, portrait, ((loli)), ((one girl)), cute face, hidden hands, asymmetrical bangs, beautiful detailed eyes, eye shadow, hair ornament, ribbons, bowties, buttons, pleated skirt, (((masterpiece))), ((best quality)), colorful|((part of the head)), ((((mutated hands and fingers)))), deformed, blurry, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, ugly, poorly drawn hands, missing limb, blurry, floating limbs, disconnected limbs, malformed hands, blur, out of focus, long neck, long body, Octane renderer, lowres, bad anatomy, bad hands, text')
    print(url)