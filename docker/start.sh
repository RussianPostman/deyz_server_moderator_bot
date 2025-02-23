#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset
 
alembic upgrade head
uvicorn api_project.composites.api:app --host 0.0.0.0 --reload
