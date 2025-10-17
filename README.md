# P3 – Administração de Sistemas e Redes: Exercícios ej1–ej4

Este repositório contém quatro exercícios independentes (shell e Python) com pastas de testes. Abaixo estão o objetivo, funcionamento, requisitos e instruções de execução de cada exercício, além de formas de validar a saída.

Sumário
- Pré‑requisitos
- Estrutura do repositório
- Exercício 1 — ej1.sh (formatação numérica k/M/G)
- Exercício 2 — ej2.sh (comparação linha a linha)
- Exercício 3 — ej3.py (k‑means 1D)
- Exercício 4 — ej4.py (refatoração de C por tipo de retorno)
- Dicas de uso no Windows e no VS Code

## Pré‑requisitos

- Python 3.8+ (para ej3.py e ej4.py)
- Ferramentas GNU (para os scripts .sh):
  - Linux/macOS: já disponíveis (bash, sed, awk)
  - Windows: usar Git Bash ou WSL (Windows Subsystem for Linux). Alternativas: MSYS2 ou Cygwin
- GCC opcional (para compilar os exemplos C do ej4): MinGW‑w64 no Windows, ou gcc no Linux/macOS

## Estrutura do repositório

- ej1.sh, ej2.sh, ej3.py, ej4.py
- ej1teste/ (arquivos de entrada/saída de exemplo)
- ej2teste/ (arquivos para comparação de exemplo)
- ej3teste/ (dados de exemplo e saídas esperadas para k‑means)
- ej4teste/
  - ejemplo1/, ejemplo2/, ejemplo3/ (programas C de exemplo, scripts e saídas esperadas)

Caminho base no seu ambiente: c:\Users\mathe\Downloads\P3.Administracion.Sys.Redes

## Exercício 1 — ej1.sh (formatação numérica k/M/G)

Objetivo
- Converter números inteiros em linhas para notação humanizada com 1 casa decimal e sufixos:
  - 4–6 dígitos → k
  - 7–9 dígitos → M
  - 10–12 dígitos → G
- Usa vírgula como separador decimal.

Como funciona
- Três expressões regulares sed aplicadas em pipeline:
  1) 10–12 dígitos: gera “X,Y G”
  2) 7–9 dígitos: gera “X,Y M”
  3) 4–6 dígitos: gera “X,Y k”
- Linhas fora desses tamanhos são mantidas sem alteração.

Exemplos
- 1234 → 1,2 k
- 4500 → 4,5 k
- 1234567 → 1,2 M
- 9876543210 → 9,8 G

Como executar
- Linux/macOS (bash):
  - bash ej1.sh ej1teste/numeros.txt > saida.txt
- Windows (Git Bash):
  - cd /c/Users/mathe/Downloads/P3.Administracion.Sys.Redes
  - bash ej1.sh ej1teste/numeros.txt > saida.txt
- Windows (WSL):
  - cd /mnt/c/Users/mathe/Downloads/P3.Administracion.Sys.Redes
  - bash ej1.sh ej1teste/numeros.txt > saida.txt

Validação (saída esperada)
- Compare com ej1teste/resultados.txt
  - Linux/macOS/Git Bash: diff -u ej1teste/resultados.txt saida.txt
  - Windows PowerShell (usando fc): fc /N ej1teste\resultados.txt .\saida.txt

## Exercício 2 — ej2.sh (comparação linha a linha)

Objetivo
- Comparar dois arquivos texto, linha a linha, e reportar diferenças indicando o número da linha e o conteúdo em cada lado.

Como funciona
- awk armazena as linhas do primeiro arquivo e compara com as linhas na mesma posição do segundo arquivo.
- Para cada linha que difere, imprime:
  - * Las lineas N difieren
  - <- linha_do_arquivo1
  - -> linha_do_arquivo2
- Observações:
  - Linhas extras no segundo arquivo serão reportadas com “<- ” vazio.
  - Linhas extras apenas no primeiro arquivo não são reportadas.

Exemplo de saída
- Para arquivos em que a linha 2 difere:
  - * Las lineas 2 difieren
  - <- B
  - -> X

Como executar
- Linux/macOS (bash):
  - bash ej2.sh ej2teste/a.txt ej2teste/b.txt
- Windows (Git Bash):
  - bash ej2.sh ej2teste/a.txt ej2teste/b.txt
- Windows (WSL):
  - bash ej2.sh ej2teste/a.txt ej2teste/b.txt

Validação
- O script imprime somente as diferenças. Use também diff/fc se desejar um comparativo completo.

## Exercício 3 — ej3.py (k‑means 1D)

Objetivo
- Agrupar números 1D com k‑means:
  - Inicializa centros com os K primeiros dados.
  - Itera atribuição/atualização até os centros não mudarem.
  - Imprime “valor<TAB>cluster” com rótulos 1..K.

Como funciona
- atribuir_etiquetas: para cada x, encontra o centro mais próximo (distância absoluta).
- atualizar_centros: recalcula cada centro como a média dos pontos atribuídos.
- Para K inválido (<= 0 ou > N), o script aborta.

Como executar
- Linux/macOS:
  - python3 ej3.py ej3teste/ejemplo1.txt 2 > out.txt
- Windows PowerShell:
  - python .\ej3.py .\ej3teste\ejemplo1.txt 2 > out.txt
- Windows (Git Bash/WSL):
  - python3 ej3.py ej3teste/ejemplo1.txt 2 > out.txt

Saída esperada
- Saídas de referência estão em:
  - ej3teste/ejemplo1_k2.txt
  - ej3teste/ejemplo1_k3.txt
  - ej3teste/ejemplo1_k4.txt
  - ej3teste/ejemplo2_k20.txt
- Valide com:
  - diff -u ej3teste/ejemplo1_k2.txt out.txt
  - fc /N ej3teste\ejemplo1_k2.txt .\out.txt

Notas
- Como os centros são floats, a convergência é testada por igualdade exata entre iterações. Nos dados fornecidos, isso é suficiente. Em cenários ruidosos, tolerâncias podem ser necessárias.

## Exercício 4 — ej4.py (refatoração de C por tipo de retorno)

Objetivo
- Ler um arquivo .c, detectar funções pelo tipo de retorno e:
  - Manter funções int in‑line no arquivo de saída.
  - Extrair funções void e float para arquivos separados:
    - void/NOME.c dentro da pasta void/
    - float/NOME.c dentro da pasta float/
  - Incluir os arquivos extraídos com #include "void/NOME.c" ou "float/NOME.c" no arquivo de saída.

Como funciona (resumo)
- Classifica linhas por regex:
  - #include, vazio, “código” genérico e declarações de funções: void|float|int NOME(...)
- Ao encontrar uma declaração de função, junta seu corpo até a próxima declaração ou include.
- Para void/float:
  - Se o arquivo destino ainda não existe, escreve a função nesse arquivo e inclui no .c de saída.
  - Se já existe, mantém a função in‑line no .c de saída (evita sobrescrever).
- Para int: mantém in‑line no .c de saída.

Limitações conhecidas
- Reconhecimento simples por regex (linhas devem começar com o tipo/declaração).
- Não analisa chaves/braces profundamente, nem protótipos vs. definições.
- Apenas tipos de retorno void, float e int são tratados explicitamente.

Como executar (exemplos prontos)
- Ejemplo 1:
  - Linux/macOS:
    - cd ej4teste/ejemplo1
    - python3 ../../ej4.py -i programa1.c -o saida1.c
  - Windows PowerShell:
    - cd .\ej4teste\ejemplo1
    - python ..\..\ej4.py -i programa1.c -o saida1.c
- Ejemplo 2:
  - python ../../ej4.py -i programa2.c -o saida2.c
- Ejemplo 3:
  - python ../../ej4.py -i programa3.c -o saida3.c

Após rodar
- Pastas void/ e/ou float/ serão criadas com as funções extraídas.
- O arquivo de saída saidaX.c conterá includes para os arquivos extraídos e o restante do código in‑line.
- Compare com as saídas de referência:
  - diff -u salida1.c saida1.c
  - fc /N .\salida1.c .\saida1.c

Compilação (opcional)
- gcc -Wall -Wextra -std=c11 saida1.c -o programa1
- No Windows (MinGW‑w64): gcc -Wall -Wextra -std=c11 .\saida1.c -o programa1.exe

## Dicas de uso no Windows e no VS Code

- Git Bash: clique direito na pasta → Git Bash Here; rode bash ejX.sh ...
- WSL: abra o terminal Ubuntu no VS Code (Remote – WSL) e rode os scripts normalmente.
- PowerShell:
  - Para Python: python .\ej3.py ... e python .\ej4.py ...
  - Para comparar arquivos: fc /N caminho\esperado.txt caminho\obtido.txt
- VS Code:
  - Terminal integrado (Ctrl+`), rode os comandos na raiz do projeto.
  - Use “Abrir Pasta” e navegue pelos diretórios ej1teste–ej4teste para executar os exemplos.
  - Se precisar, torne scripts executáveis no Linux/macOS: chmod +x ej1.sh ej2.sh

```// filepath: c:\Users\mathe\Downloads\P3.Administracion.Sys.Redes\README.md
# P3 – Administração de Sistemas e Redes: Exercícios ej1–ej4

Este repositório contém quatro exercícios independentes (shell e Python) com pastas de testes. Abaixo estão o objetivo, funcionamento, requisitos e instruções de execução de cada exercício, além de formas de validar a saída.

Sumário
- Pré‑requisitos
- Estrutura do repositório
- Exercício 1 — ej1.sh (formatação numérica k/M/G)
- Exercício 2 — ej2.sh (comparação linha a linha)
- Exercício 3 — ej3.py (k‑means 1D)
- Exercício 4 — ej4.py (refatoração de C por tipo de retorno)
- Dicas de uso no Windows e no VS Code

## Pré‑requisitos

- Python 3.8+ (para ej3.py e ej4.py)
- Ferramentas GNU (para os scripts .sh):
  - Linux/macOS: já disponíveis (bash, sed, awk)
  - Windows: usar Git Bash ou WSL (Windows Subsystem for Linux). Alternativas: MSYS2 ou Cygwin
- GCC opcional (para compilar os exemplos C do ej4): MinGW‑w64 no Windows, ou gcc no Linux/macOS

## Estrutura do repositório

- ej1.sh, ej2.sh, ej3.py, ej4.py
- ej1teste/ (arquivos de entrada/saída de exemplo)
- ej2teste/ (arquivos para comparação de exemplo)
- ej3teste/ (dados de exemplo e saídas esperadas para k‑means)
- ej4teste/
  - ejemplo1/, ejemplo2/, ejemplo3/ (programas C de exemplo, scripts e saídas esperadas)

Caminho base no seu ambiente: c:\Users\mathe\Downloads\P3.Administracion.Sys.Redes

## Exercício 1 — ej1.sh (formatação numérica k/M/G)

Objetivo
- Converter números inteiros em linhas para notação humanizada com 1 casa decimal e sufixos:
  - 4–6 dígitos → k
  - 7–9 dígitos → M
  - 10–12 dígitos → G
- Usa vírgula como separador decimal.

Como funciona
- Três expressões regulares sed aplicadas em pipeline:
  1) 10–12 dígitos: gera “X,Y G”
  2) 7–9 dígitos: gera “X,Y M”
  3) 4–6 dígitos: gera “X,Y k”
- Linhas fora desses tamanhos são mantidas sem alteração.

Exemplos
- 1234 → 1,2 k
- 4500 → 4,5 k
- 1234567 → 1,2 M
- 9876543210 → 9,8 G

Como executar
- Linux/macOS (bash):
  - bash ej1.sh ej1teste/numeros.txt > saida.txt
- Windows (Git Bash):
  - cd /c/Users/mathe/Downloads/P3.Administracion.Sys.Redes
  - bash ej1.sh ej1teste/numeros.txt > saida.txt
- Windows (WSL):
  - cd /mnt/c/Users/mathe/Downloads/P3.Administracion.Sys.Redes
  - bash ej1.sh ej1teste/numeros.txt > saida.txt

Validação (saída esperada)
- Compare com ej1teste/resultados.txt
  - Linux/macOS/Git Bash: diff -u ej1teste/resultados.txt saida.txt
  - Windows PowerShell (usando fc): fc /N ej1teste\resultados.txt .\saida.txt

## Exercício 2 — ej2.sh (comparação linha a linha)

Objetivo
- Comparar dois arquivos texto, linha a linha, e reportar diferenças indicando o número da linha e o conteúdo em cada lado.

Como funciona
- awk armazena as linhas do primeiro arquivo e compara com as linhas na mesma posição do segundo arquivo.
- Para cada linha que difere, imprime:
  - * Las lineas N difieren
  - <- linha_do_arquivo1
  - -> linha_do_arquivo2
- Observações:
  - Linhas extras no segundo arquivo serão reportadas com “<- ” vazio.
  - Linhas extras apenas no primeiro arquivo não são reportadas.

Exemplo de saída
- Para arquivos em que a linha 2 difere:
  - * Las lineas 2 difieren
  - <- B
  - -> X

Como executar
- Linux/macOS (bash):
  - bash ej2.sh ej2teste/a.txt ej2teste/b.txt
- Windows (Git Bash):
  - bash ej2.sh ej2teste/a.txt ej2teste/b.txt
- Windows (WSL):
  - bash ej2.sh ej2teste/a.txt ej2teste/b.txt

Validação
- O script imprime somente as diferenças. Use também diff/fc se desejar um comparativo completo.

## Exercício 3 — ej3.py (k‑means 1D)

Objetivo
- Agrupar números 1D com k‑means:
  - Inicializa centros com os K primeiros dados.
  - Itera atribuição/atualização até os centros não mudarem.
  - Imprime “valor<TAB>cluster” com rótulos 1..K.

Como funciona
- atribuir_etiquetas: para cada x, encontra o centro mais próximo (distância absoluta).
- atualizar_centros: recalcula cada centro como a média dos pontos atribuídos.
- Para K inválido (<= 0 ou > N), o script aborta.

Como executar
- Linux/macOS:
  - python3 ej3.py ej3teste/ejemplo1.txt 2 > out.txt
- Windows PowerShell:
  - python .\ej3.py .\ej3teste\ejemplo1.txt 2 > out.txt
- Windows (Git Bash/WSL):
  - python3 ej3.py ej3teste/ejemplo1.txt 2 > out.txt

Saída esperada
- Saídas de referência estão em:
  - ej3teste/ejemplo1_k2.txt
  - ej3teste/ejemplo1_k3.txt
  - ej3teste/ejemplo1_k4.txt
  - ej3teste/ejemplo2_k20.txt
- Valide com:
  - diff -u ej3teste/ejemplo1_k2.txt out.txt
  - fc /N ej3teste\ejemplo1_k2.txt .\out.txt

Notas
- Como os centros são floats, a convergência é testada por igualdade exata entre iterações. Nos dados fornecidos, isso é suficiente. Em cenários ruidosos, tolerâncias podem ser necessárias.

## Exercício 4 — ej4.py (refatoração de C por tipo de retorno)

Objetivo
- Ler um arquivo .c, detectar funções pelo tipo de retorno e:
  - Manter funções int in‑line no arquivo de saída.
  - Extrair funções void e float para arquivos separados:
    - void/NOME.c dentro da pasta void/
    - float/NOME.c dentro da pasta float/
  - Incluir os arquivos extraídos com #include "void/NOME.c" ou "float/NOME.c" no arquivo de saída.

Como funciona (resumo)
- Classifica linhas por regex:
  - #include, vazio, “código” genérico e declarações de funções: void|float|int NOME(...)
- Ao encontrar uma declaração de função, junta seu corpo até a próxima declaração ou include.
- Para void/float:
  - Se o arquivo destino ainda não existe, escreve a função nesse arquivo e inclui no .c de saída.
  - Se já existe, mantém a função in‑line no .c de saída (evita sobrescrever).
- Para int: mantém in‑line no .c de saída.

Limitações conhecidas
- Reconhecimento simples por regex (linhas devem começar com o tipo/declaração).
- Não analisa chaves/braces profundamente, nem protótipos vs. definições.
- Apenas tipos de retorno void, float e int são tratados explicitamente.

Como executar (exemplos prontos)
- Ejemplo 1:
  - Linux/macOS:
    - cd ej4teste/ejemplo1
    - python3 ../../ej4.py -i programa1.c -o saida1.c
  - Windows PowerShell:
    - cd .\ej4teste\ejemplo1
    - python ..\..\ej4.py -i programa1.c -o saida1.c
- Ejemplo 2:
  - python ../../ej4.py -i programa2.c -o saida2.c
- Ejemplo 3:
  - python ../../ej4.py -i programa3.c -o saida3.c

Após rodar
- Pastas void/ e/ou float/ serão criadas com as funções extraídas.
- O arquivo de saída saidaX.c conterá includes para os arquivos extraídos e o restante do código in‑line.
- Compare com as saídas de referência:
  - diff -u salida1.c saida1.c
  - fc /N .\salida1.c .\saida1.c

Compilação (opcional)
- gcc -Wall -Wextra -std=c11 saida1.c -o programa1
- No Windows (MinGW‑w64): gcc -Wall -Wextra -std=c11 .\saida1.c -o programa1.exe

## Dicas de uso no Windows e no VS Code

- Git Bash: clique direito na pasta → Git Bash Here; rode bash ejX.sh ...
- WSL: abra o terminal Ubuntu no VS Code (Remote – WSL) e rode os scripts normalmente.
- PowerShell:
  - Para Python: python .\ej3.py ... e python .\ej4.py ...
  - Para comparar arquivos: fc /N caminho\esperado.txt caminho\obtido.txt
- VS Code:
  - Terminal integrado (Ctrl+`), rode os comandos na raiz do projeto.
  - Use “Abrir Pasta” e navegue pelos diretórios ej1teste–ej4teste para executar os exemplos.
  - Se precisar, torne scripts executáveis no Linux/macOS: chmod +x ej1.sh ej2.sh
