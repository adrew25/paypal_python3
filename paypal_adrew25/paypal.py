import requests

class PayPalAPI:
    def __init__(self, settings):
        self.settings = settings

    def get_access_token(self):
        
        url = self.settings.paypal_token_url
        auth = (self.settings.paypal_client_id, self.settings.paypal_client_secret)
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(url, auth=auth, data=data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            return token
        else:
            print("Failed to retrieve access token:", response.text)
            return None
