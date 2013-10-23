from datetime import datetime
from time import sleep
from random import randint

from azure_config import *
from blast_config import *
from download_blast_database import make_sure_blast_database_is_downloaded
from run_blast_command import run_blast
from upload_to_blast_viewer import upload_to_blast_viewer
from get_next_blast_request import *
from log_blast_result import *

input_num = randint(1,200)
sleep_seconds = 60*5 # 5 minutes 
timeout_seconds = 60*15 # 15 minutes

def now():
   return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



make_sure_blast_database_is_downloaded()

while True:
    print('about to access queue (@ %s)...' % now())
    msg = get_next_blast_request(timeout_seconds)
    print('get_next_blast_request returned (@ %s)' % now())
    if msg.body == None:
        print("No message returned (timeout)")
        print("Will processing a RANDOM INPUT after sleeping for %d seconds" % sleep_seconds)
        time.sleep(sleep_seconds)
        input_num = randint(1,200)
    else:
        print("Message body = %s" % msg.body)
        input_num = int(msg.body)

    print('run_blast(%d)' % input_num)
    output_file_path = run_blast(input_num)
    print('uploading "%s" to blast viewer' % output_file_path)
    hash = upload_to_blast_viewer(output_file_path)
    url = 'http://bov.bioinfo.cas.unt.edu/cgi-bin/viewhits.cgi?hash=%s' % hash
    print('url = %s' % hash)
    log_blast_result(input_num, url)

