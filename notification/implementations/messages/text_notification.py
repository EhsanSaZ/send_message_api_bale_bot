from balebot.models.messages import TextMessage


class TextMessageNotification:
    def __init__(self, text, receiver, receiver_id, receiver_access_hash, receiver_type, notification_number):
        self.text = text
        self.receiver = receiver
        self.receiver_type = receiver_type
        self.receiver_id = receiver_id
        self.receiver_access_hash = receiver_access_hash
        self.notification_number = notification_number

    def get_json_obj(self):
        return {"type": "text",
                "receiver": self.receiver,
                "receiver_type": self.receiver_type,
                "receiver_id": self.receiver_id,
                "receiver_access_hash": self.receiver_access_hash,
                "text": self.text,
                "notification_number": self.notification_number
                }

    def get_text_message(self):
        return TextMessage(self.text)
