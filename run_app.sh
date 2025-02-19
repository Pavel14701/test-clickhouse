#!/bin/bash
# -*- coding: utf-8 -*-

# Set environment variables
export $(grep -v '^#' .env | xargs) || { echo "Error setting environment variables"; exit 1; }
export PYTHONPATH=$(pwd) || { echo "Error setting PYTHONPATH"; exit 1; }

# Run main application script
python3 app/src/main.py || { echo "Error running main.py script"; exit 1; }
if [ $? -eq 0 ]; then
    echo 'Application startup complete.'
fi
