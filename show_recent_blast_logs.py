from datetime import *
from ticks import *
from azure.storage import TableService
from blast_config import *
from azure_config import *

ts = TableService(azure_storage_account_name, azure_storage_account_key)
ts.create_table(table_name)

look_back_minutes = 15

def calc_start_time():
    today = datetime.today()
    start_time = today - timedelta(minutes=look_back_minutes)
    return start_time

def show_recent_blast_logs():
    start_time = calc_start_time()
    start_tick = str(ticks_since_epoch(start_time))
    table_query = "PartitionKey ge '%s'" % start_tick
    entities = ts.query_entities(table_name, table_query)
    print("%d BLAST jobs completed in approx past %d minutes" % (len(entities), look_back_minutes))
    print("%s - %s - %s" % ("RowKey (input_num)", "Url", "UrlExpiration"))
    for entity in entities:
        print("%s - %s - %s" % (entity.RowKey, entity.Url, entity.UrlExpiration))

show_recent_blast_logs()

