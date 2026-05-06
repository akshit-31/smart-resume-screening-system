import os
from app import create_app

app = create_app()

# Ensure secret key is set for sessions
if not os.getenv('SECRET_KEY'):
    app.secret_key = 'vercel-fallback-secret-key-change-me'

if __name__ == '__main__':
    app.run()
