from notification.implementations.messages.file_notification import FileMessageNotification
from notification.implementations.messages.text_notification import TextMessageNotification
from notification.constants.receiver_type_enum import ReceiverType


class NotificationModelFactory:
    notification_number = 0

    @staticmethod
    def create_notification(request):
        receiver = request.form.get('to')
        receiver_id = request.form.get('channel_id')
        receiver_access_hash = request.form.get('channel_access_hash')
        if request.form.get('type') == 'text':
            # (receiver, receiver_type, is_channel) = (receiver, ReceiverType.id, request.form.get('is_channel'))
            NotificationModelFactory.notification_number += 1
            return TextMessageNotification(text=request.form.get('text'), receiver=receiver,
                                           receiver_type=ReceiverType.id, receiver_id=receiver_id,
                                           receiver_access_hash=receiver_access_hash,
                                           notification_number=NotificationModelFactory.notification_number)
        if request.form.get('type') == 'file':
            caption = request.form.get('caption') if not request.form.get('caption') == '' else ' '
            file = request.files['file']
            NotificationModelFactory.notification_number += 1
            return FileMessageNotification(caption=caption, file=file.read(), mimetype=file.mimetype,
                                           name=file.filename, receiver=receiver, receiver_type=ReceiverType.id,
                                           receiver_id=receiver_id, receiver_access_hash=receiver_access_hash,
                                           notification_number=NotificationModelFactory.notification_number)
