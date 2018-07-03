from notification.implementations.sm_stopper import SMStopper
from notification.implementations.sm_starter import SMStarter
from notification.implementations.sm_notification_checker import SMNotificationChecker
from notification.implementations.flask_app import app, server_notification_queue, client_notification_queue
from notification.implementations.server_actor import ServerActor

from notification.notification_sender import NotificationSender

if __name__ == "__main__":
    notification_sender = NotificationSender(
        starter=SMStarter(),
        stopper=SMStopper(),
        notification_checker=SMNotificationChecker(),
        server_notification_queue=server_notification_queue,
        client_notification_queue=client_notification_queue,
        flask_app=app,
        server_actor=ServerActor)

    notification_sender.start()
