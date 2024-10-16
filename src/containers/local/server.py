from dotenv import load_dotenv
# Load environment variables from the custom .env file
load_dotenv(dotenv_path='.env-local')

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, reloader=True)