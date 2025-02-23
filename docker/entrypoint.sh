#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

postgres_ready() {
python << END
import sys

import psycopg2

try:
    psycopg2.connect(
        dbname="${DATABASE_NAME}",
        user="${DATABASE_USER}",
        password="${DATABASE_PASS}",
        host="${DATABASE_HOST}",
        port="${DATABASE_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

alembic upgrade head
uvicorn api_project.composites.api:app --host 0.0.0.0 --reload