from src import app
import sys


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Entre com o número da porta que deseja iniciar o servidor")
    else:
        app.run(host="localhost", port=sys.argv[1], debug=True)
