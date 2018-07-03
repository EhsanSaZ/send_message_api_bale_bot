import logging
import graypy

from notification.config.log_config import LogConfig


class NotificationLogger:
    logger = None

    @staticmethod
    def init_logger():

        use_graylog = LogConfig.use_graylog
        source = LogConfig.source
        graylog_host = LogConfig.graylog_host
        graylog_port = LogConfig.graylog_port
        log_level = LogConfig.log_level
        log_facility_name = LogConfig.log_facility_name

        temp_logger = logging.getLogger(log_facility_name)
        temp_logger.setLevel(log_level)

        log_handlers = []

        if use_graylog == "0" and graylog_host and graylog_port is not None and isinstance(graylog_port, int):
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s  %(filename)s:%(lineno)d  %(levelname)s:\n"%(message)s"'
            )
            handler.setFormatter(formatter)
            log_handlers.append(handler)

        elif use_graylog == "1":
            log_handlers.append(graypy.GELFHandler(host=graylog_host, port=graylog_port, localname=source))

        elif use_graylog == "2" and graylog_host and graylog_port is not None and isinstance(graylog_port, int):
            handler1 = graypy.GELFHandler(host=graylog_host, port=graylog_port, localname=source)

            handler2 = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s  %(filename)s:%(lineno)d  %(levelname)s:\n"%(message)s"'
            )
            handler2.setFormatter(formatter)

            log_handlers.append(handler1)
            log_handlers.append(handler2)

        for log_handler in log_handlers:
            temp_logger.addHandler(log_handler)

        NotificationLogger.logger = temp_logger
        return NotificationLogger.logger

    @staticmethod
    def get_logger():
        if NotificationLogger.logger:
            return NotificationLogger.logger
        else:
            return NotificationLogger.init_logger()
