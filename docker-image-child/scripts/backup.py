from google.cloud import storage
from datetime import datetime
import os
import re
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


def upload_many_blobs_with_transfer_manager(
    bucket_name, filenames, source_directory="",blob_name_prefix="", workers=8
):
    """Upload every file in a list to a bucket, concurrently in a process pool.

    Each blob name is derived from the filename, not including the
    `source_directory` parameter. For complete control of the blob name for each
    file (and other aspects of individual blob metadata), use
    transfer_manager.upload_many() instead.
    """

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # A list (or other iterable) of filenames to upload.
    # filenames = ["file_1.txt", "file_2.txt"]

    # The directory on your computer that is the root of all of the files in the
    # list of filenames. This string is prepended (with os.path.join()) to each
    # filename to get the full path to the file. Relative paths and absolute
    # paths are both accepted. This string is not included in the name of the
    # uploaded blob; it is only used to find the source files. An empty string
    # means "the current working directory". Note that this parameter allows
    # directory traversal (e.g. "/", "../") and is not intended for unsanitized
    # end user input.
    # source_directory=""

    # The maximum number of processes to use for the operation. The performance
    # impact of this value depends on the use case, but smaller files usually
    # benefit from a higher number of processes. Each additional process occupies
    # some CPU and memory resources until finished. Threads can be used instead
    # of processes by passing `worker_type=transfer_manager.THREAD`.
    # workers=8

    from google.cloud.storage import Client, transfer_manager
    os.environ['https_proxy'] = 'http://googleapis-dev.gcp.cloud.hk.hsbc:3128'

    storage_client = storage.Client(project='hsbc-11002897-optifinops-dev')
    bucket = storage_client.bucket(bucket_name)

    results = transfer_manager.upload_many_from_filenames(
        bucket, filenames, source_directory=source_directory, blob_name_prefix=blob_name_prefix, max_workers=workers
    )

    for name, result in zip(filenames, results):
        # The results list is either `None` or an exception for each filename in
        # the input list, in order.

        if isinstance(result, Exception):
            print("Failed to upload {} due to exception: {}".format(name, result))
        else:
            print("Uploaded {} to {}.".format(name, bucket.name))

def archive_files(src_dir, backup_dir,date):
    dest_dir=f'{backup_dir}/{date}'
    print(f'DEST: {dest_dir} SRC: {src_dir}')
    shutil.make_archive(dest_dir, 'gztar', src_dir)
# ========================== MAIN =======================================

bucket_name='turbo_backup'
now=datetime.now().strftime('%Y%m%d-%H%M%S')
print(f'START: {now}')

# upload_blob(bucket_name, '/scripts/script.sh', fr'/{now}/scripts/script.sh')

# thefiles=get_file_list('/pvcs')
# # thefiles=get_file_list('.')


mount_dir='/pvcs'
backup_dir='/turbo-backup'
print(f'archives: {get_file_list(backup_dir)}')

debug=True
# debug=False
# if debug:
#     shortlist=thefiles[10:20]
#     print( [re.sub(f'{mount_dir}/','',file) for file in shortlist])
#     upload_many_blobs_with_transfer_manager(bucket_name, [re.sub(f'{mount_dir}/','',file) for file in shortlist], source_directory=mount_dir, blob_name_prefix=f'{now}/')
#     print(len(shortlist))
# else:
#     print( [re.sub(f'{mount_dir}/','',file) for file in thefiles])
#     upload_many_blobs_with_transfer_manager(bucket_name, [re.sub(f'{mount_dir}/','',file) for file in thefiles], source_directory=mount_dir, blob_name_prefix=f'{now}/')
#     print(len(thefiles))

# blobs=get_blobs(bucket_name,f'{now}')
# print(len(blobs))
archive_files(mount_dir, backup_dir,now)

print(f'archives: {get_file_list(backup_dir)}')
    

print(f'  END: {datetime.now().strftime('%Y%m%d-%H%M%S')}')
