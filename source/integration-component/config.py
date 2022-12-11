import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "api.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "d9874b1c9d7d19b255c72a8096ecbd331f6885e9"
    LC_ALL = os.environ.get("LC_ALL")
    LANG = os.environ.get("LANG")
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_RUN_HOST = os.environ.get("FLASK_RUN_HOST")
    FLASK_RUN_PORT = os.environ.get("FLASK_RUN_PORT")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    VIDEO_ANALYTICS_URI = os.environ.get("VIDEO_ANALYTICS_URI")
    GATES_URI = os.environ.get("GATES_URI")


class TestingConfig(Config):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "test_api.db")
    TESTING = True


class StagingConfig(Config):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "staging_api.db")


app_config = {"testing": TestingConfig, "staging": StagingConfig, "development": Config}
