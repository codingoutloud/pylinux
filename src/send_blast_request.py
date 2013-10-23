from random import randint

from azure_config import *
from get_next_blast_request import *

sleep_seconds = 60 

while True:
    input_num = randint(1,200)
    print("Sending %d request to blast" % input_num)
    send_blast_request(input_num)
    print("Sleeping for %d seconds" % sleep_seconds)
    time.sleep(sleep_seconds)

