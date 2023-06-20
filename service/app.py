from src import app
from flasgger import Swagger
import sys


if __name__ == '__main__':  
    if (len(sys.argv) != 2):
        print("Entre com o número da porta que deseja iniciar o servidor")
    else:
        swagger = Swagger(app)
        app.run(host="localhost", port=sys.argv[1], debug=True)
