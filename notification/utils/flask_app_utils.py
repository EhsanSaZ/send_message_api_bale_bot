from notification.config.notification_config import NotificationConfig

ALLOWED_EXTENSIONS = NotificationConfig.allowed_extensions


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

