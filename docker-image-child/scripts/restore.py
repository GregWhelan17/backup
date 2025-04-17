from google.cloud import storage
from datetime import datetime
import os
import re
import sys
import shutil


def get_file_list(dir):
    filelist=[]
    for (root,dirs,files) in os.walk(dir,topdown=True):
        # print(f"Directory path: {root}, Directory Names: {dirs}, Files Names: {files}")
        for file in files:
            filelist.append(f'{root}/{file}')
    return filelist


def list_all_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"
    os.environ['https_proxy'] = 'http://googleapis-dev.gcp.cloud.hk.hsbc:3128'

    storage_client = storage.Client(project='hsbc-11002897-optifinops-dev')

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        print(blob.name)


def get_blobs(bucket_name, prefix):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"
    os.environ['https_proxy'] = 'http://googleapis-dev.gcp.cloud.hk.hsbc:3128'

    storage_client = storage.Client(project='hsbc-11002897-optifinops-dev')

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)

    # Note: The call returns a response only when the iterator is consumed.
    bloblist=[]
    for blob in blobs:
        print(blob.name)
        bloblist.append(blob.name)
    return bloblist


def download_many_blobs_with_transfer_manager(
        bucket_name, blob_names, destination_directory="",blob_name_prefix="", workers=8
):

    from google.cloud.storage import Client, transfer_manager
    os.environ['https_proxy'] = 'http://googleapis-dev.gcp.cloud.hk.hsbc:3128'

    storage_client = storage.Client(project='hsbc-11002897-optifinops-dev')
    bucket = storage_client.bucket(bucket_name)

    results = transfer_manager.download_many_to_path(
        bucket, blob_names, destination_directory, blob_name_prefix, max_workers=workers
    )
    print(results)
    for name, result in zip(blob_names, results):
        # The results list is either `None` or an exception for each filename in
        # the input list, in order.

        if isinstance(result, Exception):
            print("Failed to download {} due to exception: {}".format(name, result))
        else:
            print("Downloaded {} to {}.".format(name, destination_directory))

def restore_files(source_dir, dest_dir,archive_name):
    shutil.unpack_archive(f'{source_dir}/{archive_name}.tar.gz', dest_dir, 'gztar')

def clear_pvcs(dir):
    # Clear the mount directory
    filelist=[]
    dirlist=[]
    for (root,dirs,files) in os.walk(dir,topdown=True,followlinks=True):
        # print(f"Directory path: {root}, Directory Names: {dirs}, Files Names: {files}")
        for file in files:
            filelist.append(f'{root}/{file}')
        for dir in dirs:
            dirlist.append(f'{root}/{dir}')
            
    for file in filelist:
        # print(file)
        listfile=file.split('/')
        # print(listfile)
        # print(len(listfile))
        if len(listfile)==4:
            print(f'DELETE FILE: {file}')
            os.remove(file)

    for dir in dirlist:
        # print(dir)
        listdir=dir.split('/')
        # print(listdir)
        # print(len(listdir))
        if len(listdir)==4:
            print(f'DELETE DIR: {dir}')
            shutil.rmtree(dir, onerror=ondelerror)
# ========================== MAIN =======================================

bucket_name='turbo_backup'
now=datetime.now().strftime('%Y%m%d-%H%M%S')
print(f'START: {now}')
print(sys.argv[1])
archive_name=sys.argv[1]
print(f'archive_name: {archive_name}')

mount_dir='/pvcs-test'
bkup_dir='/turbo-backup'
restore_files(bkup_dir, mount_dir, archive_name)
clear_pvcs(mount_dir)




print(f'  END: {datetime.now().strftime('%Y%m%d-%H%M%S')}')