from typing import Any
import requests
import json
import openai

class OpenAIUtil:

    @staticmethod
    def models() -> str:
        return OpenAIUtil.sendRequest("/models", None, "GET")
    
    @staticmethod
    def model(modelId:str) -> str:
        return OpenAIUtil.sendRequest("/models/" + modelId, None, "GET")
    
    @staticmethod
    def sendRequest(api:str, payload:dict[str, Any] = None, method:str = "POST") -> str:
        url = openai.api_base + api
        headers = {"Authorization": "Bearer " + openai.api_key}
        if method == "POST":
            headers["Content-Type"] = "application/json"
        response = requests.request(method, url, data=json.dumps(payload) if payload else None, headers=headers)
        if response.status_code == 200:
            return response.text
        
        return None