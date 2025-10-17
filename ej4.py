#!/usr/bin/env python3

import argparse
import os
import re
import sys


RE_INCLUDE = re.compile(r'^\s*#\s*include\b')
RE_VOID = re.compile(r'^\s*void\s+([A-Za-z_]\w*)\s*\(')
RE_FLOAT = re.compile(r'^\s*float\s+([A-Za-z_]\w*)\s*\(')
RE_INT = re.compile(r'^\s*int\s+([A-Za-z_]\w*)\s*\(')
RE_EMPTY = re.compile(r'^\s*$')

def ler_arquivo(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.readlines()

def escrever_arquivo(caminho, conteudo):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)

def classificar_linha(linha):
    if RE_INCLUDE.match(linha):
        return "include", None
    m = RE_VOID.match(linha)
    if m:
        return "void_decl", m.group(1)
    m = RE_FLOAT.match(linha)
    if m:
        return "float_decl", m.group(1)
    m = RE_INT.match(linha)
    if m:
        return "int_decl", m.group(1)
    if RE_EMPTY.match(linha):
        return "empty", None
    return "code", None

def processar(entrada, saida):
    linhas = ler_arquivo(entrada)
    blocos = []
    i = 0

    while i < len(linhas):
        tipo, nome = classificar_linha(linhas[i])


        if tipo == "include" or tipo == "code" or tipo == "empty":
            blocos.append({"tipo": tipo, "texto": linhas[i]})
            i += 1
            continue


        if tipo in ("void_decl", "float_decl", "int_decl"):
            retorno = (
                "void" if tipo == "void_decl"
                else "float" if tipo == "float_decl"
                else "int"
            )
            decl = linhas[i]
            corpo = []
            i += 1


            while i < len(linhas):
                tipo2, _ = classificar_linha(linhas[i])
                if tipo2 in ("void_decl", "float_decl", "int_decl", "include"):
                    break
                corpo.append(linhas[i])
                i += 1

            blocos.append({
                "tipo": "func",
                "retorno": retorno,
                "nome": nome,
                "decl": decl,
                "corpo": "".join(corpo)
            })

    saida_buffer = []

    for b in blocos:

        if b["tipo"] in ("include", "code", "empty"):
            saida_buffer.append(b["texto"])
            continue


        ret = b["retorno"]
        nome = b["nome"]
        decl = b["decl"]
        corpo = b["corpo"]

        if ret == "int":

            saida_buffer.append(decl + corpo)
        else:
            subdir = ret
            caminho = os.path.join(subdir, f"{nome}.c")


            if not os.path.exists(caminho):
                escrever_arquivo(caminho, decl + corpo)
                saida_buffer.append(f'#include "{subdir}/{nome}.c"\n')
            else:

                saida_buffer.append(decl + corpo)


    with open(saida, 'w', encoding='utf-8') as f:
        f.write("".join(saida_buffer))

def main():
    parser = argparse.ArgumentParser(description="Desglose de funciones void/float e inclusión automática")
    parser.add_argument("-i", required=True, help="arquivo C de entrada")
    parser.add_argument("-o", required=True, help="arquivo C de saída")
    args = parser.parse_args()

    try:
        if not os.path.isfile(args.i):
            raise FileNotFoundError(f"Arquivo não encontrado: {args.i}")
        processar(args.i, args.o)
    except Exception as e:
        parser.print_help(sys.stderr)
        sys.exit(f"Erro: {e}")

if __name__ == "__main__":
    main()
