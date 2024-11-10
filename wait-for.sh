#!/bin/sh

# wait-for.sh

set -e

# Получаем хост и порт из первого аргумента
host_port="$1"
shift
cmd="$@"

# Разделяем хост и порт
host=$(echo "$host_port" | cut -d':' -f1)
port=$(echo "$host_port" | cut -d':' -f2)

# Проверяем, что порт был передан
if [ -z "$port" ]; then
  echo "Port is required. Usage: /bin/wait-for.sh <host:port> <command>"
  exit 1
fi

until nc -z "$host" "$port"; do
  echo "Waiting for $host on port $port..."
  sleep 1
done

>&2 echo "$host is up - executing command"
exec $cmd
