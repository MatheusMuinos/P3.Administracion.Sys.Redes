#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Uso: $0 <arquivo_de_numeros>" >&2
  exit 1
fi

sed -E 's/^([0-9]{1,3})([0-9])([0-9]{8})$/\1,\2 G/' "$1" \
| sed -E 's/^([0-9]{1,3})([0-9])([0-9]{5})$/\1,\2 M/' \
| sed -E 's/^([0-9]{1,3})([0-9])([0-9]{2})$/\1,\2 k/'
