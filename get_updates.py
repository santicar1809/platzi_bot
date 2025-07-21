import requests


def get_updates(token, offset=None):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {'timeout':100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()['result']
