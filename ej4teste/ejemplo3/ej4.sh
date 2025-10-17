#!/usr/bin/env bash
set -euo pipefail

rm -rf void float salida_test.c 2>/dev/null || true

echo "=== PRUEBA EJ4 ==="
echo "→ Ejecutando: ./ej4.py -i programa1.c -o salida_test.c"
./ej4.py -i programa1.c -o salida_test.c

echo
if diff -b salida_test.c salida1.c >/dev/null; then
  echo "✅ salida1.c correcto"
else
  echo "❌ salida1.c difiere"
  diff -y --suppress-common-lines salida_test.c salida1.c || true
fi

echo
if diff -b float/suma.c suma.c >/dev/null; then
  echo "✅ float/suma.c correcto"
else
  echo "❌ float/suma.c difiere"
  diff -y --suppress-common-lines float/suma.c suma.c || true
fi

echo
if diff -b void/imprime.c imprime.c >/dev/null; then
  echo "✅ void/imprime.c correcto"
else
  echo "❌ void/imprime.c difiere"
  diff -y --suppress-common-lines void/imprime.c imprime.c || true
fi

echo
echo "✅ Prueba completada."
