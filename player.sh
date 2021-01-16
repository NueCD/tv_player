#!/bin/bash

# Working directory.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

# Autoupdate
git pull

# File with the queue.
QUEUE="queue"

# Create queue file.
[[ -f "$QUEUE" ]] && rm $QUEUE ; touch $QUEUE

# Start queueing webserver.
python web_server.py &
PY_PID=$!

# Cleanup finction.
function finish {
    kill $PY_PID
    pkill mpv
}
trap finish EXIT

# Main loop.
while :; do
    # Get first link in queue and play it if there is any.
    VID=$(head -n 1 $QUEUE)
    if [[ "$VID" != "" ]]; then
        mpv $VID --fs
    
        # Remove the link that was played.
        tail -n +2 $QUEUE > "$QUEUE.tmp" && mv "$QUEUE.tmp" $QUEUE
    else
        # Wait a bit if there is nothing to play.
        sleep 5
    fi
done
