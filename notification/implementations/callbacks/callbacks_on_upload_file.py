from notification.implementations.callbacks.callbacks_on_send_messages import *


def file_upload_success(result, user_data):
    notification = user_data['kwargs']['notification']
    logger = user_data['kwargs']['logger']
    bot = user_data['kwargs']['bot']
    ack_queue = user_data['kwargs']['ack_queue']

    notification.file_id = str(user_data.get("file_id", None))
    notification.file_access_hash = str(user_data.get("user_id", None))
    message = notification.get_file_message()
    if message:

        kwargs = {"notification": notification, "logger": logger,
                  "ack_queue": ack_queue}
        bot.send_message(message, user_data['kwargs']['peer'], success_callback=success_callback_on_send_message,
                         failure_callback=failure_callback_on_send_message,
                         kwargs=kwargs)
        logger.debug(
            "send file notification {} to user or channel {} at : {}".format(notification.get_json_obj(),
                                                                             notification.receiver,
                                                                             datetime.now()))
    else:
        logger.error("can not create file message notification for peer {}  : {}".format(notification.receiver,
                                                                                         datetime.now()))


def file_upload_failure(response, user_data):
    notification = user_data['kwargs']['notification']
    logger = user_data['kwargs']['logger']
    ack_queue = user_data['kwargs']['ack_queue']
    ack = AckNotification(description_code=response.body.code, description_tag=response.body.tag,
                          notification_number=notification.notification_number,
                          success_flag=False)
    ack_queue.put(ack)
    logger.error(
        "failed to upload file for notification {}in file_upload_failure at : {}".format(
            notification.get_json_obj(), datetime.now()))
