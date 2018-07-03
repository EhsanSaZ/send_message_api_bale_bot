import queue
import traceback

from balebot.models.base_models import Peer
from balebot.models.constants.peer_type import PeerType

from notification.implementations.callbacks.callbacks_on_upload_file import *
from notification.implementations.callbacks.callbacks_on_send_messages import *
from notification.implementations.messages.file_notification import FileMessageNotification
from notification.implementations.messages.text_notification import TextMessageNotification
from notification.strategy.notification_checker import NotificationChecker


class SMNotificationChecker(NotificationChecker):
    def check_notification(self, notification_sender):
        notification_sender.logger.debug(
            "network connected: {}".format(notification_sender.updater.network_connected()))
        try:
            a_notification = notification_sender.notification_queue.get(False)  # doesn't block
        except queue.Empty:  # raised when queue is empty
            a_notification = None

        if a_notification:
            try:
                if isinstance(a_notification, TextMessageNotification):
                    notification_sender.logger.debug(
                        "get notification {} from queue at : {}".format(a_notification.get_json_obj(),
                                                                        datetime.now()))
                    group_peer = Peer(peer_type=PeerType.group, peer_id=a_notification.receiver_id,
                                      access_hash=a_notification.receiver_access_hash)
                    kwargs = {"notification": a_notification, "logger": notification_sender.logger,
                              "ack_queue": notification_sender.ack_queue}
                    notification_sender.bot.send_message(a_notification.get_text_message(), group_peer,
                                                         success_callback=success_callback_on_send_message,
                                                         failure_callback=failure_callback_on_send_message,
                                                         kwargs=kwargs)
                elif isinstance(a_notification, FileMessageNotification):
                    notification_sender.logger.debug("get new file notification from queue: {}".format(datetime.now()))

                    group_peer = Peer(peer_type=PeerType.group, peer_id=a_notification.receiver_id,
                                      access_hash=a_notification.receiver_access_hash)
                    kwargs = {"notification": a_notification, "bot": notification_sender.bot,
                              "logger": notification_sender.logger, "peer": group_peer,
                              "ack_queue": notification_sender.ack_queue}
                    notification_sender.bot.upload_file(file=a_notification.file, file_type="file",
                                                        success_callback=file_upload_success,
                                                        failure_callback=file_upload_failure,
                                                        kwargs=kwargs)
                    notification_sender.logger.debug(
                        "send upload request for file notification  {} for channel {} in"
                        " success_callback_on_find_channel\tchannel peer: {}\tat : {}".format(
                            a_notification.get_json_obj(), a_notification.receiver, group_peer.get_json_object(),
                            datetime.now()))

                notification_sender.logger.debug("notofication handled : {}".format(datetime.now()))

            except Exception as ex:
                notification_sender.logger.error(ex)
                traceback.print_exc()
        else:
            notification_sender.logger.debug(" no notification in queue at time: {}".format(datetime.now()))
