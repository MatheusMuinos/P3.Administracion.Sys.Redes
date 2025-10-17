#!/usr/bin/env bash
set -euo pipefail

test_diff() {
  local salida="$1"
  local ref="$2"
  local desc="$3"
  if diff -b "$salida" "$ref" >/dev/null; then
    echo "✅ $desc correcto"
  else
    echo "❌ $desc difiere"
    diff -y --suppress-common-lines "$salida" "$ref" || true
  fi
}

echo "=== PRUEBAS EJEMPLO 1 ==="

for k in 2 3 4; do
  echo "→ Ejecutando ./ej3.py ejemplo1.txt $k"
  ./ej3.py ejemplo1.txt "$k" > "salida_k${k}.txt"
  test_diff "salida_k${k}.txt" "ejemplo1_k${k}.txt" "EJEMPLO1 K=$k"
done

echo
echo "=== PRUEBA EJEMPLO 2 ==="
echo "→ Ejecutando ./ej3.py ejemplo2.txt 20"
./ej3.py ejemplo2.txt 20 > salida_k20.txt
test_diff salida_k20.txt ejemplo2_k20.txt "EJEMPLO2 K=20"

echo
echo "✅ Pruebas completadas."
