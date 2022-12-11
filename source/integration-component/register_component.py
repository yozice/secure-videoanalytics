import argparse
import os
import uuid

import jwt
from backend.models import Component
from config import app_config
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from global_variables import db

load_dotenv()

parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)
parser.add_argument("component_name")  # positional argument

config_name = os.getenv("FLASK_ENV", "default")

SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": None,
    "pool_recycle": None,
}

app = Flask(__name__)
app.config.from_object(app_config[config_name])
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


migrate = Migrate(app, db, render_as_batch=True)  # obj for db migrations
CORS(app)


if __name__ == "__main__":
    args = parser.parse_args()

    with app.app_context():
        user = Component.query.filter_by(component_name=args.component_name).first()
        if not user:
            new_user = Component(
                public_id=str(uuid.uuid4()), component_name=args.component_name
            )
            db.session.add(new_user)
            db.session.commit()
    token = jwt.encode({"public_id": user.public_id}, app.config["SECRET_KEY"], "HS256")
    output_token_file = f"./tokens/{args.component_name}.txt"
    os.makedirs(os.path.dirname(output_token_file), exist_ok=True)
    with open(output_token_file, "w+") as f:
        f.write(token)
