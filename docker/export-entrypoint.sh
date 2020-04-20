#!/bin/bash
set -euxo pipefail

declare -p | grep -e ACCESS_KEY -e SECRET_KEY -e S3_BUCKET > /app/.aws

cron -f
