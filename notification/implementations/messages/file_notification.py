import sys

from balebot.models.messages import PhotoMessage, DocumentMessage, TextMessage


class FileMessageNotification:
    def __init__(self, caption, file, mimetype, name, receiver,receiver_id, receiver_access_hash, receiver_type, notification_number):
        self.caption = caption
        self.file = file
        self.mimetype = mimetype
        self.name = name
        self.receiver = receiver
        self.receiver_type = receiver_type
        self.receiver_id = receiver_id
        self.receiver_access_hash = receiver_access_hash
        self.file_id = None
        self.file_access_hash = None
        self.notification_number = notification_number

    def get_json_obj(self):
        return {"type": "file",
                "receiver": self.receiver,
                "receiver_type": self.receiver_type,
                "receiver_id": self.receiver_id,
                "receiver_access_hash": self.receiver_access_hash,
                "name": self.name,
                "mimetype": self.mimetype,
                "caption": self.caption,
                "file_id": self.file_id,
                "file_access_hash": self.file_access_hash,
                "notification_number": self.notification_number
                }

    def get_file_message(self):
        if self.file_access_hash is not None and self.file_id is not None:
            if self.mimetype.startswith("image/"):
                return PhotoMessage(file_id=self.file_id,
                                    access_hash=self.file_access_hash,
                                    name=self.name,
                                    file_size=sys.getsizeof(self.file),
                                    mime_type=self.mimetype,
                                    caption_text=TextMessage(self.caption),
                                    file_storage_version=1,
                                    thumb=None)
            else:
                return DocumentMessage(file_id=self.file_id, access_hash=self.file_access_hash,
                                       name=self.name,
                                       file_size=sys.getsizeof(self.file),
                                       mime_type=self.mimetype,
                                       caption_text=TextMessage(text=self.caption),
                                       file_storage_version=1)
        else:
            return None
