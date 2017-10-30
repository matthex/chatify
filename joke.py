import requests

def get_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {
        'accept': "application/json"
        }
    response = requests.request("GET", url, headers=headers).json()
    return response['joke']