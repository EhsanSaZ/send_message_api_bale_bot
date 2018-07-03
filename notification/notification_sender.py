import asyncio
from balebot.updater import Updater
from notification.config.notification_config import NotificationConfig
from notification.parameters import Parameters
from notification.utils.notification_logger import NotificationLogger


class NotificationSender:
    def __init__(self,
                 starter,
                 stopper,
                 notification_checker,
                 server_notification_queue,
                 client_notification_queue,
                 flask_app,
                 server_actor,
                 **kwargs):
        self.extra_parameters = Parameters(**kwargs)

        self.starter = starter
        self.stopper = stopper

        self.notification_checker = notification_checker

        self.flask_app = flask_app
        self.server_actor_ref = server_actor.start(self.flask_app)

        self.logger = NotificationLogger.get_logger()
        self.async_loop = asyncio.get_event_loop()

        self.updater = Updater(token=NotificationConfig.notification_token, loop=self.async_loop)

        self.bot = self.updater.bot
        self.dispatcher = self.updater.dispatcher

        self.running = True

        self.perform_check_failure_counter = 0
        self.total_send_failure_counter = 0
        self.notification_queue = server_notification_queue
        self.ack_queue = client_notification_queue

    def check(self):
        if self.running:
            self.notification_checker.check_notification(notification_sender=self)
            self.async_loop.call_later(NotificationConfig.check_interval, self.check)

    def start(self):
        self.starter.start(notification_sender=self, server_actor_ref=self.server_actor_ref)

    def stop(self):
        self.stopper.stop(notification_sender=self, server_actor_ref=self.server_actor_ref)
