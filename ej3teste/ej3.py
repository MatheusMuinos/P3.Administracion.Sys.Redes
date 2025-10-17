#!/usr/bin/env python3

import argparse

def atribuir_etiquetas(dados, centros):
    etiquetas = []
    for x in dados:
        menor_dist = abs(x - centros[0])
        etiqueta = 1
        for j in range(1, len(centros)):
            dist = abs(x - centros[j])
            if dist < menor_dist:
                menor_dist = dist
                etiqueta = j + 1
        etiquetas.append(etiqueta)
    return etiquetas


def atualizar_centros(dados, etiquetas, K, centros_antigos):
    soma = [0.0] * K
    cont = [0] * K
    for x, lab in zip(dados, etiquetas):
        j = lab - 1
        soma[j] += x
        cont[j] += 1
    novos = centros_antigos[:]
    for j in range(K):
        if cont[j] > 0:
            novos[j] = soma[j] / cont[j]
    return novos


def main():
    parser = argparse.ArgumentParser(description="Algoritmo k-means 1D")
    parser.add_argument("arquivo", help="arquivo com dados (um número por linha)")
    parser.add_argument("K", type=int, help="número de clusters (inteiro positivo)")
    args = parser.parse_args()

    # Lê os dados do arquivo
    try:
        with open(args.arquivo, "r", encoding="utf-8") as f:
            dados = [int(l.strip()) for l in f if l.strip()]
    except Exception as e:
        parser.error(f"Erro ao ler o arquivo: {e}")

    if args.K <= 0 or args.K > len(dados):
        parser.error("K deve ser positivo e menor ou igual ao número de dados")

    # Inicializa centros com os K primeiros dados
    K = args.K
    centros = [float(dados[i]) for i in range(K)]

    # Itera até convergir
    while True:
        antigos = centros[:]
        etiquetas = atribuir_etiquetas(dados, centros)
        centros = atualizar_centros(dados, etiquetas, K, antigos)
        if centros == antigos:
            break

    # Imprime resultado final
    for x, lab in zip(dados, etiquetas):
        print(f"{x}\t{lab}")


if __name__ == "__main__":
    main()
