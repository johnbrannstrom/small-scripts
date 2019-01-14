#!/bin/bash

# Startup actions
<script> &

# Shutdown actions
shutdown_action() {
    # Actions to take for shutting down
    exit 0
}
# Wait for shutdown signal
trap shutdown_action SIGINT SIGTERM

while true
do
    sleep 1
done
