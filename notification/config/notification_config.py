import os


class NotificationConfig:
    check_interval = float(os.environ.get('CHECK_INTERVAL', None) or "0.5")
    notification_token = os.environ.get('TOKEN', None) or "6ecbbb63231ed7dbc95f4e0cd176f3951bb0b1b3"
    flask_port = os.environ.get('FLASK_PORT', None) or "8086"
    time_out_wait_for_check_client_queue = int(os.environ.get('TIME_OUT_WAIT_FOR_CHECK_CHECK_CLIENT_QUEUE', None) or "60")#time in second
    time_out_for_block_on_client_queue = int(os.environ.get('TIME_OUT_FOR_BLOCK_ON_CLIENT_QUEUE', None) or "5")
    allowed_extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xml', 'bmp', 'svg', 'ods', 'xlr', 'xls',
                      'xlsx', 'mp4', 'mkv', 'mp3', 'doc', 'docx']
