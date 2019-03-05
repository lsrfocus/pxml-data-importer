#!/usr/bin/env bash
set -exo pipefail

# Add any setup scripts here, e.g. data dump/load.
#
# For reference, see https://neo4j.com/docs/operations-manual/current/tools/dump-load/
# and https://stackoverflow.com/questions/45166636/create-neo4j-databse-from-backup-inside-neo4j-docker
#
# Example (uncomment to export your local database):
#
#DATE_FORMAT=$(date +%Y-%m-%d-%H-%M-%S)
#bin/neo4j-admin dump --database=graph.db --to=data/db-${DATE_FORMAT}.dump
