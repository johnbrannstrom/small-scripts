#!/bin/bash

# Copy files to destination with SFTP

# SFTP batch file with commands
SFTP_BATCH_FILE="sftp_deploy_files"

# Check for destination host
if [ ${1} == "" ]; then
    echo "Error: user@host missing!"
    exit 1
fi
USER_HOST=${1}

# Check for destination path
DST_PATH="/path/to/project/"
if [ "${2}" != "" ]; then
    DST_PATH=${2}
fi

echo "sftp -b ${SFTP_BATCH_FILE} ${USER_HOST}:${DST_PATH}"
sftp -b ${SFTP_BATCH_FILE} ${USER_HOST}:${DST_PATH}
