#!/bin/bash
# -*- coding: utf-8 -*-

# Set environment variables
export $(grep -v '^#' .env | xargs) || { echo "Error setting environment variables"; exit 1; }
export PYTHONPATH=$(pwd) || { echo "Error setting PYTHONPATH"; exit 1; }

# Create database if not exists
curl -u admin:admin1234 -X POST 'http://localhost:8123/?query=CREATE+DATABASE+IF+NOT+EXISTS+people_in_space' -H 'Content-Length: 0' || { echo "Exception in database creation"; exit 1; }
if [ $? -eq 0 ]; then
    echo 'Creation of database people_in_space complete.'
fi

# Run tables creation script
python3 app/src/infrastructure/models/tables_creation.py || { echo "Error running tables_creation.py script"; exit 1; }
if [ $? -eq 0 ]; then
    echo 'Tables creation complete.'
fi
