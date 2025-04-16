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
    

    # ========================== MAIN =======================================

    bucket_name='turbo_backup'
    now=datetime.now().strftime('%Y%m%d-%H%M%S')
    print(f'START: {now}')
    print(sys.argv[1])
    print(sys.argv[1].split('/'))
    print(sys.argv[1].split('/')[-1])
    print(sys.argv[1].split('/')[-2])
    selected=sys.argv[1].split('/')[-2]
    print(f'SELECTED: {selected}')


    # list_all_blobs(bucket_name)
    # # upload_blob(bucket_name, '/scripts/script.sh', fr'/{now}/scripts/script.sh')

    # thefiles=get_file_list('/pvcs')
    # # # thefiles=get_file_list('.')

    # # print(f'=========================\n{thefiles}\n=========================')

    # # totalSize=0
    # # for file in thefiles:
    # #     totalSize+=os.path.getsize(file)
    # #     target=file.replace('/pvcs', now)
    # #     print(f'copy {file} bucket:{target}')
    # # size=totalSize / 1000000000
    # # print(f'Length: {len(thefiles)}, Size: {totalSize}, Size Gb: {size}')

    # # print(f'========================= thefiles END =========================')
    mount_dir='/pvcs'

    # debug=True
    # # debug=False
    # if debug:
    #     shortlist=thefiles[10:20]
    #     print( [re.sub(f'{mount_dir}/','',file) for file in shortlist])
    #     upload_many_blobs_with_transfer_manager(bucket_name, [re.sub(f'{mount_dir}/','',file) for file in shortlist], source_directory=mount_dir, blob_name_prefix=f'/{now}/')
    #     print(len(shortlist))
    # else:
    #     print( [re.sub(f'{mount_dir}/','',file) for file in thefiles])
    #     upload_many_blobs_with_transfer_manager(bucket_name, [re.sub(f'{mount_dir}/','',file) for file in thefiles], source_directory=mount_dir, blob_name_prefix=f'/{now}/')
    #     print(len(thefiles))

    # blobs=get_blobs(bucket_name,f'{selected}/')

    blobs=get_blobs(bucket_name,selected)
    print(len(blobs))
    download_many_blobs_with_transfer_manager(
        bucket_name,  [re.sub(f'{selected}/','',blob) for blob in blobs], destination_directory=f"{mount_dir}/",blob_name_prefix=f'{selected}/', workers=8
    )
    filelist=get_file_list(mount_dir)
    print(filelist)

    print(f'  END: {datetime.now().strftime('%Y%m%d-%H%M%S')}')