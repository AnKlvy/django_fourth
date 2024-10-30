#!/bin/sh

# wait-for.sh

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 5432; do
  echo "Waiting for $host..."
  sleep 1
done

>&2 echo "$host is up - executing command"
exec $cmd
