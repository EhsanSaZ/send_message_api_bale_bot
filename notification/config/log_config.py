import logging
import os


class LogConfig:
    # 0:print to output          1:use graylog      2:both 0 and 1
    use_graylog = os.environ.get('NOTIFICATION_BOT_USE_GRAYLOG', None) or "0"
    source = os.environ.get('SOURCE', None) or "send_message_api"
    graylog_host = os.environ.get('NOTIFICATION_BOT_GRAYLOG_HOST', None) or "0.0.0.0"
    graylog_port = int(os.environ.get('NOTIFICATION_BOT_GRAYLOG_PORT', None) or 12201)
    log_level = int(os.environ.get('NOTIFICATION_BOT_LOG_LEVEL', None) or logging.DEBUG)
    log_facility_name = os.environ.get('NOTIFICATION_BOT_LOG_FACILITY_NAME', None) or "notification_bot"
