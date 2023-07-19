from flask.cli import FlaskGroup
from flasgger import Swagger
from src import app, db

swagger = Swagger(app)
cli = FlaskGroup(app)

# # RECRIA TODO O BANCO
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    cli()