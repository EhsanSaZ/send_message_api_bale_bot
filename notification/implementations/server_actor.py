import pykka
from notification.config.notification_config import NotificationConfig
from flask import request


class ServerActor(pykka.ThreadingActor):
    def __init__(self, flask_app):
        super(ServerActor, self).__init__()
        self.flask_app = flask_app

    def on_receive(self, message):
        print(self.message)

    def run(self):
        self.flask_app.run(host='0.0.0.0', port=NotificationConfig.flask_port)

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
