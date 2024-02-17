import requests
from .config import Settings
class PayPalAPI:
    """
    A class representing the PayPal API.

    Attributes:
    - settings: An instance of the Settings class that contains the PayPal API settings.

    Methods:
    - __init__(self, settings=Settings()): Initializes a new instance of the PayPalAPI class.
    - get_access_token(self): Retrieves the access token from PayPal.
    - create_order(self, amount, currency='EUR', intent='CAPTURE', **kwargs): Creates a new order with the specified amount and currency.

    Usage:
    ```
    api = PayPalAPI()
    access_token = api.get_access_token()
    order_id = api.create_order(100.0, currency='USD')
    ```
    """

    def __init__(self, settings = Settings()):
        self.settings = settings

    def get_access_token(self):
        """
        Retrieves the access token from PayPal.

        Returns:
        - The access token as a string if successful.
        - None if failed to retrieve the access token.
        """
        
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

    def create_order(self, amount, currency=None, intent='CAPTURE', **kwargs):
        """
        Creates a new order with the specified amount and currency.

        Parameters:
        - amount: The amount of the order.
        - currency: The currency of the order. If not provided, defaults to the currency specified in settings.
        - intent: The intent of the order. Defaults to 'CAPTURE'.
        - **kwargs: Additional optional parameters for customization.

        Returns:
        - A dictionary containing the details of the created order if successful.
        
        Raises:
        - Exception: If failed to create the order.
        """
        url = kwargs.get('url', self.settings.paypal_order_url)
        
        if currency is None:
            currency = self.settings.paypal_currency
        elif currency != self.settings.paypal_currency:
            raise ValueError(f"Currency '{currency}' does not match the currency in the settings '{self.settings.paypal_currency}'")
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }
        data = {
            "intent": intent,
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": currency,
                        "value": str(amount)
                    }
                }
            ],
            "payment_source": {
                "paypal": {
                    "experience_context": {
                        "payment_method_preference": kwargs.get('payment_method_preference', "IMMEDIATE_PAYMENT_REQUIRED"),
                        "brand_name": kwargs.get('brand_name', "EXAMPLE INC"),
                        "locale": kwargs.get('locale', "en-US"),
                        "landing_page": kwargs.get('landing_page', "LOGIN"),
                        "shipping_preference": kwargs.get('shipping_preference', "SET_PROVIDED_ADDRESS"),
                        "user_action": kwargs.get('user_action', "PAY_NOW"),
                        "return_url": kwargs.get('return_url', self.settings.paypal_return_url),
                        "cancel_url": kwargs.get('cancel_url', self.settings.paypal_cancel_url)
                    }
                }
            }
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception("Failed to create order:", response.text)
