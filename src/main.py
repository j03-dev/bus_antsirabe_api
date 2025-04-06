from oxapy import HttpServer, Cors
from core.app_state import AppState
from api import routes

server = HttpServer(("0.0.0.0", 8080))
server.app_data(AppState())
server.attach(routes.api)
cors = Cors()
cors.methods = ["GET", "POST"]
server.config(cors=cors)


if __name__ == "__main__":
    server.run()
