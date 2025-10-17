#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 2 ]; then
  echo "Uso: $0 <arquivo1> <arquivo2>" >&2
  exit 1
fi

awk '
  FNR==NR { a[FNR]=$0; next }
  {
    i=FNR
    if (a[i] != $0) {
      print "* Las lineas " i " difieren"
      print "<- " a[i]
      print "-> " $0
    }
  }
' "$1" "$2"

