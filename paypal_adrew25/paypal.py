import requests
from .config import Settings
import random
import time
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
        - payment_method_preference
        - brand_name
        - locale
        - landing_page
        - shipping_preference
        - user_action
        - return_url
        - cancel_url

        Returns:
        - A dictionary containing the details of the created order if successful.
        
        Raises:
        - Exception: If failed to create the order.
        """
        url = kwargs.get('url', self.settings.paypal_order_url)
        
        if currency is None:
            currency = self.settings.paypal_currency
        elif currency != self.settings.paypal_currency:
            raise ValueError(f"Currency '{currency}' does not match the currency in the .env '{self.settings.paypal_currency}'")
        
        headers = {
            'Content-Type': 'application/json',
            # 'PayPal-Request-Id': '7b92603e-77ed-4896-8e78-5dea2050476a',
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
                        "brand_name": kwargs.get('brand_name', self.settings.paypal_brand_name),
                        "locale": kwargs.get('locale', self.settings.paypal_locale),
                        "landing_page": kwargs.get('landing_page', "GUEST_CHECKOUT"),
                        "shipping_preference": kwargs.get('shipping_preference', "NO_SHIPPING"),
                        "user_action": kwargs.get('user_action', "PAY_NOW"),
                        "return_url": kwargs.get('return_url', self.settings.paypal_return_url),
                        "cancel_url": kwargs.get('cancel_url', self.settings.paypal_cancel_url)
                    }
                }
            }
        }
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to create order:", response.text)
        
        
    def capture_order(self, order_id):
        url = f"{self.settings.paypal_order_url}/{order_id}/capture"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }
        
        response = requests.post(url, headers=headers)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception("Failed to capture order:", response.text)
        


    def show_order_details(self, order_id):
        """
        Retrieves the details of the specified order.

        Parameters:
        - order_id: The ID of the order to retrieve.

        Returns:
        - A dictionary containing the details of the order if successful.
        
        Raises:
        - Exception: If failed to retrieve the order details.
        """
        url = f"{self.settings.paypal_order_url}/{order_id}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to retrieve order Pinelodetails:", response.text)
        

    def update_order(self, order_id, data):
        """
        Updates the details of the specified order.

        Parameters:
        - order_id: The ID of the order to update.
        - data: A dictionary containing the details to update.
            - intent	replace	
            - payer	replace, add	Using replace op for payer will replace the whole payer object with the value sent in request.
            - purchase_units	replace, add	
            - purchase_units[].custom_id	replace, add, remove	
            - purchase_units[].description	replace, add, remove	
            - purchase_units[].payee.email	replace	
            - purchase_units[].shipping.name	replace, add	
            - purchase_units[].shipping.address	replace, add	
            - purchase_units[].shipping.type	replace, add	
            - purchase_units[].soft_descriptor	replace, remove	
            - purchase_units[].amount	replace	
            - purchase_units[].items	replace, add, remove	
            - purchase_units[].invoice_id	replace, add, remove	
            - purchase_units[].payment_instruction	replace	
            - purchase_units[].payment_instruction.disbursement_mode	replace	By default, disbursement_mode is INSTANT.
            - purchase_units[].payment_instruction.platform_fees	replace, add, remove	
            - purchase_units[].supplementary_data.airline	replace, add, remove	
            - purchase_units[].supplementary_data.card	replace, add, remove	
            - application_context.client_configuration	replace, add

        Returns:
        - A dictionary containing the details of the updated order if successful.
        
        Raises:
        - Exception: If failed to update the order.
        """
        url = f"{self.settings.paypal_order_url}/{order_id}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to update order:", response.text)
        

    def confirm_order(self, order_details, **kwargs):
        """
        Confirms the specified order.

        Parameters:
        - order_id: The ID of the order to confirm.
        - customer_email: The email address of the customer.
        - customer_given_name: The given name of the customer.
        - customer_surname: The surname of the customer.
        - **kwargs: Additional optional parameters for customization.
            - payment_method_preference
            - brand_name
            - locale
            - landing_page
            - shipping_preference
            - user_action
            - return_url
            - cancel_url

        Returns:
        - A dictionary containing the details of the confirmed order if successful.

        Raises:
        - Exception: If failed to confirm the order.
        """
        url = f"{self.settings.paypal_order_url}/{order_details['id']}/confirm-payment-source"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }
        payload = {
            "payment_source": {
                "paypal": {
                    "name": {
                        "given_name": kwargs.get('customer_given_name', order_details['payer']['name']['given_name']),
                        "surname": kwargs.get('customer_surname', order_details['payer']['name']['surname'])
                    },
                    "email_address": kwargs.get('customer_email', order_details['payer']['email_address']),
                    "experience_context": {
                        "payment_method_preference": kwargs.get('payment_method_preference', "IMMEDIATE_PAYMENT_REQUIRED"),
                        "brand_name": kwargs.get('brand_name', self.settings.paypal_brand_name),
                        "locale": kwargs.get('locale', self.settings.paypal_locale),
                        "landing_page": kwargs.get('landing_page', "GUEST_CHECKOUT"),
                        "shipping_preference": kwargs.get('shipping_preference', "NO_SHIPPING"),
                        "user_action": kwargs.get('user_action', "PAY_NOW"),
                        "return_url": kwargs.get('return_url', self.settings.paypal_return_url),
                        "cancel_url": kwargs.get('cancel_url', self.settings.paypal_cancel_url)
                    }
                }
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to confirm order:", response.text)



# ----------------- PAYPAL PAYMENT -----------------

    def create_payment(self, payment_value, credits):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }

        invoice_id = int(time.time() * 1000) + random.randint(1, 1000)
        
        payload = {
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [
                {
                    "amount": {
                        "total": f"{payment_value}.00",
                        "currency": "EUR"
                    },
                    "description": f"Purchase of {credits} credits in the app.",
                    "invoice_number": invoice_id,
                    "item_list": {
                        "items": [
                            {
                                "name": "App Credits",
                                "quantity": str(payment_value),
                                "price": "1",
                                "currency": "EUR"
                            }
                        ]
                    }
                }
            ],
            "note_to_payer": "Thank you for your purchase!",
            "redirect_urls": {
                "return_url": self.settings.paypal_return_url,
                "cancel_url": self.settings.paypal_cancel_url
            }
        }

        response = requests.post('https://api-m.sandbox.paypal.com/v1/payments/payment', headers=headers, json=payload)
        return response.json()


    def execute_payment_order(self, payment_id, payer_id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_access_token()}',
        }
        payload = {
            "payer_id": payer_id
        }
        response = requests.post(f'https://api-m.sandbox.paypal.com/v1/payments/payment/{payment_id}/execute', headers=headers, json=payload)
        return response.json()
