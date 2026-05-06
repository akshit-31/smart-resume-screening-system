from app import create_app

app = create_app()

# Vercel expects the app object to be named 'app'
if __name__ == '__main__':
    app.run()
