#!/bin/bash
# Fix Docker socket permissions so the jenkins user can call docker commands.
# Runs as root (via sudo), then hands off to the normal Jenkins entrypoint.
set -e

# Make docker socket accessible to all users inside the container
if [ -S /var/run/docker.sock ]; then
    chmod 666 /var/run/docker.sock
fi

# Hand off to the official Jenkins entrypoint
exec /usr/bin/tini -- /usr/local/bin/jenkins.sh "$@"
