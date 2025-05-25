from oxapy import HttpServer, Cors  # type: ignore
from app.core.app_state import AppState
from app.api import routes

server = HttpServer(("0.0.0.0", 8080))
server.app_data(AppState())
server.attach(routes.api)
server.cors(Cors())


if __name__ == "__main__":
    server.run()
