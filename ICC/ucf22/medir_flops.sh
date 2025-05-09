# Ulisses Curvello Ferreira
# GRR: 20223829
#!/bin/bash

# Verifica se o binário existe
if [ ! -f ./resolveEDO ]; then
    echo "Erro: ./resolveEDO não encontrado. Compile com 'make' antes de executar."
    exit 1
fi

# Verifica se o arquivo de entrada foi fornecido
if [ $# -ne 1 ]; then
    echo "Uso: $0 <arquivo_entrada>"
    exit 1
fi

ENTRADA="$1"

# Executa o programa com LIKWID, extrai apenas os valores desejados
likwid-perfctr -C 0 -g FLOPS_DP -m ./resolveEDO < "$ENTRADA" | \
    awk -F'|' '/FP_ARITH_INST_RETIRED_SCALAR_DOUBLE/ {
        gsub(/ /, "", $2);  # remove espaços no nome
        gsub(/ /, "", $4);  # remove espaços no valor
        printf "%s,%s\n", $2, $4
    }'
