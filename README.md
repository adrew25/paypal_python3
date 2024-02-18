# PayPal Integration Python Module

WORKING ON IT!!!
A package for paypal integration cause i am lazy to write the same code again and again.
for now i only use payment_source -> paypal

## Usage

Comming soon :)

```
    order = paypal_api.create_order(
        amount=100.0,
        currency='USD',
        intent='CAPTURE',
        description='Payment for goods',
        custom_id='123',
        shipping_preference='GET_FROM_FILE'
    )
```

## Installation

You can install the PayPal Integration Python Module using pip:
(I am working on it cause i dont know how! )

you should add a .env file to the project with the following:

```
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=
PAYPAL_TOKEN_URL=https://api-m.sandbox.paypal.com/v1/oauth2/token
PAYPAL_ORDER_URL=https://api-m.sandbox.paypal.com/v2/checkout/orders
PAYPAL_MODE=sandbox
PAYPAL_CURRENCY=USD
PAYPAL_RETURN_URL=http://0.0.0.0:8000/success
PAYPAL_CANCEL_URL=http://0.0.0.0:8000/cancel
PAYPAL_WEBHOOK_ID=
PAYPAL_WEBHOOK_URL=http://0.0.0.0:8000/webhook

```
