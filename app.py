from sqlalchemy import true
from src import create_app
from src.extensions import db
from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = create_app()
app.secret_key = getenv("SECRET_KEY")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)