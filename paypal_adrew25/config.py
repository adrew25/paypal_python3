import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        # Get the parent directory of the current directory
        project_root = self._find_project_root()
        dotenv_path = os.path.join(project_root, '.env')

        # Load values from .env file
        load_dotenv(dotenv_path)

        # Define settings using environment variables or defaults
        self.paypal_client_id = os.getenv("PAYPAL_CLIENT_ID", "YOUR_PAYPAL_CLIENT_ID")
        self.paypal_client_secret = os.getenv("PAYPAL_CLIENT_SECRET", "secret")
        self.paypal_token_url = os.getenv("PAYPAL_TOKEN_URL", "https://api-m.sandbox.paypal.com/v1/oauth2/token")
        self.paypal_order_url = os.getenv("PAYPAL_ORDER_URL", "https://api-m.sandbox.paypal.com/v2/checkout/orders")
        self.paypal_mode = os.getenv("PAYPAL_MODE", "sandbox")
        self.paypal_currency = os.getenv("PAYPAL_CURRENCY", "EUR")
        self.paypal_return_url = os.getenv("PAYPAL_RETURN_URL", "http://localhost:8000/success")
        self.paypal_cancel_url = os.getenv("PAYPAL_CANCEL_URL", "http://localhost:8000/cancel")
        self.paypal_webhook_id = os.getenv("PAYPAL_WEBHOOK_ID", "YOUR PAYPAL WEBHOOK ID")
        self.paypal_webhook_url = os.getenv("PAYPAL_WEBHOOK_URL", "http://localhost:8000/webhook")

    def _find_project_root(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        while current_dir:
            if os.path.exists(os.path.join(current_dir, '.env')):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                break  # Reached root directory
            current_dir = parent_dir
        # .env file not found in any parent directory, using current directory
        return os.path.abspath(os.path.dirname(__file__))

    def custom_settings(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self
