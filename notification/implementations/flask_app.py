import queue
import traceback
import time

from flask import Flask, flash, json, Response, request
from datetime import datetime
from notification.implementations.messages.notification_message_factory import NotificationModelFactory
from notification.utils.flask_app_utils import *
from notification.utils.notification_logger import NotificationLogger
from notification.config.notification_config import NotificationConfig

server_notification_queue = queue.Queue()
client_notification_queue = queue.Queue()
app = Flask(__name__)
app.debug = False
logger = NotificationLogger.get_logger()


@app.route('/api/v1/send_text_message', methods=['POST'])
def send_text_message():
    logger.debug("get new send text message request at : {}".format(datetime.now()))
    try:
        if request.form.get('type') == 'text':
            notification = NotificationModelFactory.create_notification(request)
            server_notification_queue.put(notification)
            t1 = time.time()
            ack = None
            while time.time() - t1 < NotificationConfig.time_out_wait_for_check_client_queue:
                try:
                    ack = client_notification_queue.get(timeout=NotificationConfig.time_out_for_block_on_client_queue)
                except queue.Empty:  # raised when queue is empty
                    ack = None

                if ack is None:
                    pass
                elif not notification.notification_number == ack.notification_number:
                    client_notification_queue.put(ack)
                else:
                    break
            if ack:
                if ack.success_flag:
                    return Response("OK", status=200)
                else:
                    if ack.description_code in [400, 403, 401, 500]:
                        return Response(
                            json.dumps(
                                {"bot_response_tag": ack.description_tag, "bot_response_code": ack.description_code}),
                            status=ack.description_code)
                    else:
                        return Response(
                            json.dumps(
                                {"bot_response_tag": ack.description_tag, "bot_response_code": ack.description_code}),
                            status=400)
            else:
                return Response("TIME_OUT_FOR_BOT_SEND_MESSAGE", status=504)
        else:
            return Response("INVALID TYPE", status=400)
    except Exception as ex:
        traceback.print_exc()
        return Response(status=500)


@app.route('/api/v1/send_file_message', methods=['POST'])
def send_file_message():
    logger.debug("get new send file message request at : {}".format(datetime.now()))
    try:
        if request.form.get('type') == 'file':
            if 'file' not in request.files:
                flash('No file part')
                return Response("No file part", status=400)
            else:
                file = request.files['file']
                if file.filename == '':
                    flash('No selected file')
                    return Response("No selected file", status=400)

                if file and allowed_file(file.filename):
                    notification = NotificationModelFactory.create_notification(request)
                    server_notification_queue.put(notification)
                    t1 = time.time()
                    ack = None
                    while time.time() - t1 < NotificationConfig.time_out_wait_for_check_client_queue:
                        try:
                            ack = client_notification_queue.get(timeout=NotificationConfig.time_out_for_block_on_client_queue)
                        except queue.Empty:  # raised when queue is empty
                            ack = None

                        if ack is None:
                            pass
                        elif not notification.notification_number == ack.notification_number:
                            client_notification_queue.put(ack)
                        else:
                            break
                    if ack:
                        if ack.success_flag:
                            return Response("OK", status=200)
                        else:
                            if ack.description_code in [400, 403, 401]:
                                return Response(
                                    json.dumps({"bot_response_tag": ack.description_tag,
                                                "bot_response_code": ack.description_code}), status=ack.description_code)
                            else:
                                return Response(
                                    json.dumps({"bot_response_tag": ack.description_tag,
                                                "bot_response_code": ack.description_code}), status=400)
                    else:
                        return Response("TIME_OUT_FOR_BOT_SEND_MESSAGE", status=504)
                else:
                    return Response("File type not allowed", status=400)
        else:
            return Response("INVALID TYPE", status=400)
    except Exception as ex:
        traceback.print_exc()
        return Response(status=500)
