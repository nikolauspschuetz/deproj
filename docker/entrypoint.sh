#!/usr/bin/env bash

set -e

if [ "$1" = 'python' ]; then
    exec "$@"
fi

exec "$@"