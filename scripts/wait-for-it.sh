#!/usr/bin/env bash
# wait-for-it.sh - wait until a TCP host:port is available

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until nc -z "$host" "$port"; do
  >&2 echo "Waiting for $host:$port..."
  sleep 1
done

>&2 echo "$host:$port is available, executing command."
exec $cmd
