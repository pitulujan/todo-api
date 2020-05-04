from api import app
from api.models import User
from dotenv import load_dotenv


load_dotenv(".env")

if __name__ == "__main__":
    app.run(debug=True)
