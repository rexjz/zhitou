#!/usr/bin/env bash

set -euo pipefail

COMMIT_HASH=$(git rev-parse --short HEAD)

REPO="crpi-rodg8r18boez6uld.cn-shanghai.personal.cr.aliyuncs.com/max3xu/zhitou-api"

TAG_LATEST="${REPO}:latest"
TAG_COMMIT="${REPO}:${COMMIT_HASH}"

echo "构建镜像：${TAG_LATEST}"
docker build . -f deploy/test/Dockerfile.api \
  -t "${TAG_LATEST}" \
  -t "${TAG_COMMIT}"

echo "推送镜像：${TAG_LATEST}"
docker push "${TAG_LATEST}"

echo "推送镜像：${TAG_COMMIT}"
docker push "${TAG_COMMIT}"

echo "构建并推送完成: latest, ${COMMIT_HASH}"
