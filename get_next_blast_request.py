from azure.servicebus import * 
from blast_config import *
from azure_config import *

sbs = ServiceBusService(service_bus_namespace,
                        service_bus_key,
                        'owner')

sbs.create_queue(request_queue_name)
sbs.create_queue(response_queue_name)

peek_lock = False

def get_next_blast_request(timeout_seconds = 30):
    msg = sbs.receive_queue_message(request_queue_name, peek_lock, timeout_seconds)
    return msg

def mark_blast_request_completed(msg):
    if peek_lock:
        msg.delete()

def send_blast_request(input_num):
    msg1 = Message(str(input_num))
    sbs.send_queue_message(request_queue_name, msg1)

