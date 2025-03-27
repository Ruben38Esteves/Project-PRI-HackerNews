#!/bin/bash
set -e

# Start Solr with the given arguments (e.g., precreate core)
solr-precreate "$@" &

# Wait for Solr to start
until curl --silent --head --fail http://localhost:8983/solr; do
    echo "Waiting for Solr to start..."
    sleep 5
done

# Populate Solr with initial data
echo "Populating Solr with initial data..."
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../scraper/jsons/limpo.json" \
    "http://localhost:8983/solr/news/update?commit=true"

echo "Data population complete!"
