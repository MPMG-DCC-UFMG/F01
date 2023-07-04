from flask.cli import FlaskGroup
from flasgger import Swagger
from src import app, db

swagger = Swagger(app)
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()