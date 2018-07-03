from datetime import datetime
from notification.implementations.messages.ack_notification import AckNotification


def success_callback_on_send_message(response, user_data):
    notification = user_data['kwargs']['notification']
    logger = user_data['kwargs']['logger']
    ack_queue = user_data['kwargs']['ack_queue']
    ack = AckNotification(description_code=None, description_tag=None,
                          notification_number=notification.notification_number,
                          success_flag=True)
    ack_queue.put(ack)
    logger.debug(
        "put ack for  notification {} in success_callback_on_send_message\tat : {}".format(
            notification.get_json_obj(), datetime.now()))
    logger.debug(
        "send text notification {} to number {} at : {}".format(notification.get_json_obj(),
                                                                notification.receiver,
                                                                datetime.now()))
    # print(response)
    # print(user_data)


def failure_callback_on_send_message(response, user_data):
    notification = user_data['kwargs']['notification']
    logger = user_data['kwargs']['logger']
    ack_queue = user_data['kwargs']['ack_queue']
    ack = AckNotification(description_code=response.body.code, description_tag=response.body.tag,
                          notification_number=notification.notification_number,
                          success_flag=False)
    ack_queue.put(ack)
    logger.warning(
        "failed to send message for notification {}in failure_callback_send_message : {}".format(
            notification.get_json_obj(), datetime.now()))
