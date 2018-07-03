class AckNotification:
    def __init__(self, description_code, description_tag, notification_number, success_flag):
        self.description_code = description_code
        self.description_tag = description_tag
        self.notification_number = notification_number
        self.success_flag = success_flag
