#!/bin/bash

# Load environment variables from .env file
set -a  # automatically export all variables
source .env
set +a  # disable auto-export

echo "Environment variables loaded."