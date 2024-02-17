import os

# Create .env file
with open('.env', 'w') as env_file:
    env_file.write('PAYPAL_CLIENT_ID=\n')
    env_file.write('PAYPAL_CLIENT_SECRET=\n')
    env_file.write('PAYPAL_MODE=sandbox\n')
    env_file.write('PAYPAL_CURRENCY=EUR\n')
    env_file.write('PAYPAL_RETURN_URL=http://0.0.0.0:8000/success\n')
    env_file.write('PAYPAL_CANCEL_URL=http://0.0.0.0:8000/cancel\n')
    env_file.write('PAYPAL_WEBHOOK_ID=\n')
    env_file.write('PAYPAL_WEBHOOK_URL=http://0.0.0.0:8000/webhook\n')

# Export .env.example
os.system('export $(cat .env > .env.example)')
