# host=$(grep -v '^\s*#' turbohost)
# echo ${host}

threshold=${1:-75}
echo $threshold
diskfull=$(df -h | tail -n+2 | grep -v 'shm' | while read -r Filesystem Size Used Avail Percent Mounted ; do
    value=$(echo ${Percent} | sed 's/%//')
    if [ ${value} -gt ${threshold} ] ; then
        echo ${Mounted}
    fi
done)

# echo $diskfull

if [ "${diskfull}" != '' ] ; then
    echo
    echo The following filesystems are over the ${threshold}% Limit:
    df -h ${diskfull}
    echo '=============================================================================================='
    exit 1
fi
