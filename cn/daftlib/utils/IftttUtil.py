import json
import requests

class IftttUtil:

    @staticmethod
    def sendNotification(eventName:str, key:str, text:str) -> str:
        
        url = f"https://maker.ifttt.com/trigger/{eventName}/with/key/{key}"
        # url = f"https://maker.ifttt.com/trigger/{eventName}/json/with/key/{key}"
        payload = {"value1": text}
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        return response.text