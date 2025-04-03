from google.cloud import storage
from datetime import datetime
import os
import re
import sys


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

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    os.environ['https_proxy'] = 'http://googleapis-dev.gcp.cloud.hk.hsbc:3128'

    storage_client = storage.Client(project='hsbc-11002897-optifinops-dev')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

def download_many_blobs_with_transfer_manager(
        bucket_name, blob_names, destination_directory="",blob_name_prefix="", workers=8
):

    from google.cloud.storage import Client, transfer_manager
    os.environ['https_proxy'] = 'http://googleapis-dev.gcp.cloud.hk.hsbc:3128'

    storage_client = storage.Client(project='hsbc-11002897-optifinops-dev')
    bucket = storage_client.bucket(bucket_name)

    # results = transfer_manager.upload_many_from_filenames(
    #     bucket, filenames, source_directory=source_directory, blob_name_prefix=blob_name_prefix, max_workers=workers
    # )
    results = transfer_manager.download_many_to_path(
        bucket, blob_names, destination_directory, blob_name_prefix, max_workers=workers
    )

    for name, result in zip(blob_names, results):
        # The results list is either `None` or an exception for each filename in
        # the input list, in order.

        if isinstance(result, Exception):
            print("Failed to download {} due to exception: {}".format(name, result))
        else:
            print("Downloaded {} to {}.".format(name, destination_directory))
    

# ========================== MAIN =======================================

bucket_name='turbo_backup'
now=datetime.now().strftime('%Y%m%d-%H%M%S')
print(f'START: {now}')
selected=sys.argv[1].split('/')[-2]
print(f'SELECTED: {selected}')


mount_dir='/pvcs'

blobs=get_blobs(bucket_name,selected')
print(len(blobs))
download_many_blobs_with_transfer_manager(
        bucket_name,  [re.sub(f'{selected}/','',blob) for blob in blobs], destination_directory=f"{mount_dir}/",blob_name_prefix=f'{selected}/', workers=8
)

filelist=get_file_list(mount_dir)
print(filelist)


print(f'  END: {datetime.now().strftime('%Y%m%d-%H%M%S')}')