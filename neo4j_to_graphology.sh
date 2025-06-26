#!/usr/bin/env bash

# Usage: ./neo4j_to_graphology.sh [input.json] [--name "Graph Name"] [--debug]
# If no input file is given, reads from stdin. If no --name is given, defaults to 'My Graph'.

INPUT="/dev/stdin"
GRAPH_NAME="My Graph"
DEBUG=0
TMPFILE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      GRAPH_NAME="$2"
      shift 2
      ;;
    --debug)
      DEBUG=1
      shift
      ;;
    *)
      INPUT="$1"
      shift
      ;;
  esac
done

# If reading from stdin, save to a temp file for multiple jq passes
if [[ "$INPUT" == "/dev/stdin" ]]; then
  TMPFILE=$(mktemp)
  cat > "$TMPFILE"
  INPUT="$TMPFILE"
fi

if [[ $DEBUG -eq 1 ]]; then
  echo "[DEBUG] INPUT: $INPUT" >&2
  echo "[DEBUG] GRAPH_NAME: $GRAPH_NAME" >&2
fi

# Extract all unique nodes from all graph.nodes, using .properties.identifier as key
NODES=$(jq -c '
  .results[0].data[].graph.nodes[] |
  {
    id: .id,
    key: .properties.identifier,
    name: (.properties.name // .properties.symbol // ""),
    label: (.labels[0] // ""),
    url: (.properties.url // null)
  }' "$INPUT" | sort | uniq)

if [[ $DEBUG -eq 1 ]]; then
  echo "[DEBUG] NODES extracted from graph property:" >&2
  echo "$NODES" >&2
fi

# Build nodes array for Graphology
NODES_JSON=$(echo "$NODES" | jq -s -c '
  unique_by(.key) |
  map({key: .key, name: .name, label: .label, url: .url})
' | sed 's/^\[//;s/\]$//')

# Build a mapping from node id to identifier for edge lookup
ID_TO_IDENTIFIER=$(echo "$NODES" | jq -s 'map({(.id): .key}) | add')

if [[ $DEBUG -eq 1 ]]; then
  echo "[DEBUG] ID_TO_IDENTIFIER mapping:" >&2
  echo "$ID_TO_IDENTIFIER" >&2
fi

# Extract all edges from all graph.relationships, mapping startNode/endNode to identifier, and include url
EDGES=$(jq -c --argjson idmap "$ID_TO_IDENTIFIER" '
  .results[0].data[].graph.relationships[] |
  {
    source: ($idmap[.startNode]),
    target: ($idmap[.endNode]),
    reltype: .type,
    url: (.properties.url // null)
  }' "$INPUT" | sort | uniq)

if [[ $DEBUG -eq 1 ]]; then
  echo "[DEBUG] EDGES extracted from graph property (mapped to identifier):" >&2
  echo "$EDGES" >&2
fi

# Build edges array for Graphology
EDGES_JSON=$(echo "$EDGES" | jq -s -c '
  unique_by(.source, .target, .reltype, .url) |
  map({source: .source, target: .target, reltype: .reltype, url: .url})
' | sed 's/^\[//;s/\]$//')

if [[ $DEBUG -eq 1 ]]; then
  echo "[DEBUG] Outputting final Graphology JSON..." >&2
fi

printf '{\n  attributes: {name: "%s"},\n  nodes: [%s],\n  edges: [%s]\n}\n' \
  "$GRAPH_NAME" "$NODES_JSON" "$EDGES_JSON"

# Clean up temp file if used
if [[ -n "$TMPFILE" ]]; then
  rm -f "$TMPFILE"
fi 