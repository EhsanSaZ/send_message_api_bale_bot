import traceback

from notification.strategy.stopper import Stopper


class SMStopper(Stopper):
    def stop(self, notification_sender, server_actor_ref):
        notification_sender.running = False
        notification_sender.logger.warning("sd notification bot stoped")
        server_proxy = server_actor_ref.proxy()
        try:
            future = server_proxy.shutdown_server()
        except Exception as e:
            traceback.print_exc()
