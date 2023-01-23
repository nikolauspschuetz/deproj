#!/usr/bin/env bash

set -e

BUILD_TARGET=${BUILD_TARGET:=main}

BUILD_VERSION=$1
BUILD_VERSION=${BUILD_VERSION:=0.0.0}

TAG_LATEST=$2
TAG_LATEST="${TAG_LATEST:=true}"

REPOSITORY_NAME="${REPOSITORY_NAME:=deproj}"

TAGS=(-t "$REPOSITORY_NAME:$BUILD_VERSION")

if [ "$TAG_LATEST" = "true" ]; then
  TAGS+=(
    -t "$REPOSITORY_NAME:latest"
  )
fi

docker build --target "${BUILD_TARGET}" "${TAGS[@]}" .