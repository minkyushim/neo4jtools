#!/usr/bin/env bash

# Usage:
#   ./neo4j_cypher.sh --url <server_url> --user <userid> --password <password> [--query <cypher_query>] [--db <database_name>]

# Default values
DBNAME="neo4j"
QUERY=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --url)
      SERVER_URL="$2"
      shift; shift
      ;;
    --user)
      USER="$2"
      shift; shift
      ;;
    --password)
      PASS="$2"
      shift; shift
      ;;
    --query)
      QUERY="$2"
      shift; shift
      ;;
    --db)
      DBNAME="$2"
      shift; shift
      ;;
    -h|--help)
      echo "Usage: $0 --url <server_url> --user <userid> --password <password> [--query <cypher_query>] [--db <database_name>]"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 --url <server_url> --user <userid> --password <password> [--query <cypher_query>] [--db <database_name>]"
      exit 1
      ;;
  esac
done

# Check required parameters
if [[ -z "$SERVER_URL" || -z "$USER" || -z "$PASS" ]]; then
  echo "Error: --url, --user, and --password are required."
  echo "Usage: $0 --url <server_url> --user <userid> --password <password> [--query <cypher_query>] [--db <database_name>]"
  exit 1
fi

AUTH=$(echo -n "$USER:$PASS" | base64)

if [ -z "$QUERY" ]; then
  # Show server info
  curl -s "$SERVER_URL" | jq .
else
  # Get transaction endpoint from server info
  TX_URL_TEMPLATE=$(curl -s "$SERVER_URL" | jq -r '.transaction')
  if [ "$TX_URL_TEMPLATE" = "null" ]; then
    echo "Could not get transaction endpoint from server info."
    exit 2
  fi
  # Replace {databaseName} with actual db name
  TX_URL=$(echo "$TX_URL_TEMPLATE" | sed "s/{databaseName}/$DBNAME/")
  # Compose Cypher query payload
  PAYLOAD=$(jq -n --arg q "$QUERY" '{"statements":[{"statement":$q,"resultDataContents":["row","graph"]}]}')
  curl -s -H "Content-Type: application/json" \
       -H "Authorization: Basic $AUTH" \
       -d "$PAYLOAD" \
       "$TX_URL/commit" | jq .
fi