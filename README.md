# Turbonomic Backup and Restore

This is the scripts, docker image and Jenkins pipeline that backs up all the Turbonomic PV's that are mounted on Turbonomic containers to Google Cloud storage and allows the backups to be restored to turbonomic


# Image Contents

The same image is used for both backup and restore. 

* This image is build on the HSBC image `nexus3.systems.uk.hsbc:18096/com/hsbc/group/itid/es/dc/ubuntu/gcr-ubuntu-2404:latest`
* Python 3
* Public Python Modules
  * google-cloud-storage
* google cloud credentials file stored at `/root/.config/gcloud/application_default_credentials.json`



# Backup

The backup process is triggered by a Jenkins pipeline and follows the these steps:
* scale down all the turbonomic containers so the PVC's are not mounted
* Build a job yaml file based on a template, include mounts for all the PVC's that are in the namespace.
* apply the job yaml file so the job is deployed.
* The job container starts that has access to all the PVCs and runs a script
* The script transfers all the files to the storage using the following filename format: `YYMMDD_HHMMSS/PVC_name/filepath/filename`.
* The container goes to Completed status and this releases all the PVCs
* the containers log is listed in the pipeline console
* Turbonomic pods are scaled up.


The backup process has 3 components:
* A Jenkins Pipeline
* Scripts Called by the pipeline
* Kubernetes Job that launches a Docker container

## Jenkins Pipeline
* Connects to the Kubernetes cluster
* clones the git repo 
* runs the script

## Script
* calls a second script that scales down the turbo deployments to 0, stopping all the pods.
* Uses a job template to create a specification yaml that includes mounts for each PVC in the namespace and runs an script on the container
* deploys the job
* waits until the pod is complete
* echos out the log from the job's pod
* scales up the turbonomic deployments

## Kubernetes Job
The job runs a container and instructs it to run a script
The script copies all the files in all mounted PVCs to the google cloud storage


# Restore
The restore process is very similar it is also triggered by a Jenkins pipeline and follows these steps:
* scale down all the turbonomic containers so the PVC's are not mounted
* Build a job yaml file based on a template, include mounts for all the PVC's that are in the namespace.
* apply the job yaml file so the job is deployed.
* The job container starts with access to all the PVCs and runs a script
* The script optionally backs up turbonomic, clears the PVCs and then transfers all the files in the storage with the selected date to the correct PVC directory mounted on the container.
* The container goes to Completed status and this releases all the PVCs
* the containers log is listed in the pipeline console
* Turbonomic pods are scaled up.

The restore process has 3 components:
* A Jenkins Pipeline
* Scripts Called by the pipeline
* Kubernetes Job that launches a Docker container

## Jenkins Pipeline
* Connects to the Kubernetes cluster
* clones the git repo
* connects to the GCP account where the storage is
* lists the date prefixes for all the backups found on the storage
* asks the user to select from the list the backup that is to be used.
* Also asks if a backup should be performed before the restore is run
* runs the script, passing the date and backup decision.

## Script
* calls a second script that scales down the turbo deployments to 0, stopping all the pods.
* Takes a job template and includes mounts for each PVC in the namespace. Also adds the passed arguments to the script that will be run
* deploys the job
* waits until the pod is complete
* echos out the log from the job's pod
* scales up the turbonomic deployments

## Kubernetes Job
* The job runs a container and instructs it to run a script
* The script optionally runs a backup.
* The script copies all the files related to the selected backup to the mounted PVCs 

# Image Build

The image is built and pushed to a nexus repository. Once in the repository it can be deployed using the instruction here [deployment](#deployment).
To access the ubuntu and python modules, also stored in a nexus repository a secret and certificate are needed and additional options are required for the `docker build` command. the secret and certificate are included here and a `build.cmd` file is included which has the full command required to build and push the image.


# Prerequisites

* Service Account that allows the pipeline to clone the git repository
* credentials that allow the pipeline to connect to kubernetes
* credentials file for a service account that allows the container script to connect to the google cloud storage
