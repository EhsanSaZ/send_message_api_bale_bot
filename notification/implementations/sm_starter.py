from notification.strategy.starter import Starter


class SMStarter(Starter):
    def start(self, notification_sender, server_actor_ref):
        notification_sender.check()
        notification_sender.logger.debug("start run")
        server_proxy = server_actor_ref.proxy()
        future = server_proxy.run()
        notification_sender.updater.run()
        notification_sender.stop()
