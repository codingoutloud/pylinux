from datetime import *
from azure.storage import TableService
from blast_config import *
from azure_config import *

ts = TableService(azure_storage_account_name, azure_storage_account_key)
print('table_name = %s' % table_name)
ts.create_table(table_name)


def calc_expiration():
    today = datetime.today()
    expiration = today + timedelta(days=60)
    return expiration

def log_blast_result(input_num, url):
    expiration_date = calc_expiration()
    ts.insert_entity(
       table_name,
       {
          'PartitionKey' : 'blast_py_demo',
          'RowKey': str(input_num),
          'RequestNum': input_num, # store as integer
          'Url': url,
          'UrlExpirationDate': expiration_date
       }
    )
