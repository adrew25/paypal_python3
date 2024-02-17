import os
from dotenv import load_dotenv



class Settings:
    def __init__(self):
        load_dotenv()  # Load values from .env file

        self.paypal_client_id = os.getenv("PAYPAL_CLIENT_ID", "YOUR_PAYPAL_CLIENT_ID")
        self.paypal_client_secret = os.getenv("PAYPAL_CLIENT_SECRET", "secret")
        self.paypal_mode = os.getenv("PAYPAL_MODE", "sandbox")
        self.paypal_currency = os.getenv("PAYPAL_CURRENCY", "EUR")
        self.paypal_return_url = os.getenv("PAYPAL_RETURN_URL", "http://localhost:8000/success")
        self.paypal_cancel_url = os.getenv("PAYPAL_CANCEL_URL", "http://localhost:8000/cancel")
        self.paypal_webhook_id = os.getenv("PAYPAL_WEBHOOK_ID", "YOUR PAYPAL WEBHOOK ID")
        self.paypal_webhook_url = os.getenv("PAYPAL_WEBHOOK_URL", "http://localhost:8000/webhook")
        
        
    def custom_settings(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self
