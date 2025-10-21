#!/usr/bin/env python3
import argparse
import os
import re
import sys

# Padrões de reconhecimento
PATTERNS = {
    "include": re.compile(r'^\s*#\s*include\b'),
    "void": re.compile(r'^\s*void\s+([A-Za-z_]\w*)\s*\('),
    "float": re.compile(r'^\s*float\s+([A-Za-z_]\w*)\s*\('),
    "int": re.compile(r'^\s*int\s+([A-Za-z_]\w*)\s*\('),
    "empty": re.compile(r'^\s*$'),
}

def classificar_linha(linha):
    for tipo, regex in PATTERNS.items():
        if m := regex.match(linha):
            return tipo, m.group(1) if tipo in ("void", "float", "int") else None
    return "code", None

def processar(entrada, saida):
    with open(entrada, encoding='utf-8') as f:
        linhas = f.readlines()

    blocos, i = [], 0

    while i < len(linhas):
        tipo, nome = classificar_linha(linhas[i])

        # Linhas simples
        if tipo in ("include", "code", "empty"):
            blocos.append(("texto", linhas[i]))
            i += 1
            continue

        # Função encontrada
        decl = linhas[i]
        retorno, corpo = tipo, []
        i += 1

        while i < len(linhas):
            tipo2, _ = classificar_linha(linhas[i])
            if tipo2 in ("void", "float", "int", "include"):
                break
            corpo.append(linhas[i])
            i += 1

        blocos.append(("func", retorno, nome, decl, "".join(corpo)))

    # Gera saída
    saida_buffer = []
    for b in blocos:
        if b[0] == "texto":
            saida_buffer.append(b[1])
        else:
            _, ret, nome, decl, corpo = b
            if ret == "int":
                saida_buffer.append(decl + corpo)
            else:
                subdir = ret
                caminho = os.path.join(subdir, f"{nome}.c")
                os.makedirs(subdir, exist_ok=True)
                if not os.path.exists(caminho):
                    with open(caminho, 'w', encoding='utf-8') as f:
                        f.write(decl + corpo)
                    saida_buffer.append(f'#include "{subdir}/{nome}.c"\n')
                else:
                    saida_buffer.append(decl + corpo)

    with open(saida, 'w', encoding='utf-8') as f:
        f.write("".join(saida_buffer))

def main():
    parser = argparse.ArgumentParser(description="Desglose de funções void/float e inclusão automática")
    parser.add_argument("-i", required=True, help="arquivo C de entrada")
    parser.add_argument("-o", required=True, help="arquivo C de saída")
    args = parser.parse_args()

    try:
        processar(args.i, args.o)
    except Exception as e:
        sys.exit(f"Erro: {e}")

if __name__ == "__main__":
    main()
