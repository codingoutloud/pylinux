import os, platform, base64
from azure.storage import *

plat = platform.system()
print("Platform == " + plat)

#database_root_path = os.sep + "blastdb"
#database_root_path = os.path.join("d:", database_root_path)
database_root_path = "/home/azureuser/BLAST/blastdb"
print('database_root_path = %s' % database_root_path)

blob_service = BlobService(account_name='blastfileseu', account_key='xkTjP5IRpkcqlhDve95latLJIAljQmtE93cT4nidnRUJA8YRJctjFTV7gX7bYGCkGUbnD3GooMx7kUPqxbyX6Q==')
blob_container_names = ['inputncbi', 'ncbi']
blob_chunk_size = 4 * 1024 * 1024

def make_sure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def is_local(file_path, expected_size):
    if not os.path.exists(file_path):
        return False
    else:
        return os.path.getsize(file_path) >= expected_size # Windows adds a couple of bytes..

# python download methods modeled on http://www.windowsazure.com/en-us/develop/python/how-to-guides/blob-service/
def download_large_blob(blob_service, blob_container_name, blob_name, file_path):
    props = blob_service.get_blob_properties(blob_container_name, blob_name)
    blob_size = int(props['content-length']) # same as blob.properties.content_length but we don't have a blob handy

    index = 0
    with open(file_path, 'wb') as f:
        while index < blob_size:
            chunk_range = 'bytes={}-{}'.format(index, index + blob_chunk_size - 1)
            data = blob_service.get_blob(blob_container_name, blob_name, x_ms_range=chunk_range)
            length = len(data)
            index += length
            if length > 0:
                f.write(data)
                if length < blob_chunk_size:
                    break
            else:
                break

def download_small_blob(blob_service, blob_container_name, blob_name, file_path):
        stream = blob_service.get_blob(blob_container_name, blob_name)
        with open(file_path, 'w') as f:
            f.write(stream)

def download_if_needed(blob_container_name, blob, directory_path):
    file_path = os.path.join(directory_path, blob.name)
    expected_size = blob.properties.content_length

    if not is_local(file_path, expected_size):
        if expected_size < blob_chunk_size:
            download_small_blob(blob_service, blob_container_name, blob.name, file_path)
        else:
            download_large_blob(blob_service, blob_container_name, blob.name, file_path)

def download_blast_database(blob_service, database_root_path):
    make_sure_path_exists(database_root_path)

    for blob_container_name in blob_container_names:
        directory_path = os.path.join(database_root_path, blob_container_name)
        make_sure_path_exists(directory_path)

        print(blob_container_name)
        blobs = blob_service.list_blobs(blob_container_name)
        for blob in blobs:
            print("%d bytes at %s" % (blob.properties.content_length, blob.url))
            download_if_needed(blob_container_name, blob, directory_path)

download_blast_database(blob_service, database_root_path)


