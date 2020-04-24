#!/bin/bash
set -euxo pipefail

cron

exec "$@"