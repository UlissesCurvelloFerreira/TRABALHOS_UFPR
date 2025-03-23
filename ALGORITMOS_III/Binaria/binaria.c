#include <stdio.h>
#include <stdlib.h>

// Estrutura do nó da árvore
typedef struct No {
    int valor;
    struct No *esquerda, *direita;
} No;

// Função para criar um novo nó
No* criarNo(int valor) {
    No* novoNo = (No*)malloc(sizeof(No));
    novoNo->valor = valor;
    novoNo->esquerda = novoNo->direita = NULL;
    return novoNo;
}

// Função para inserir um valor na árvore
No* inserir(No* raiz, int valor) {
    if (raiz == NULL) {
        return criarNo(valor);
    }
    if (valor < raiz->valor) {
        raiz->esquerda = inserir(raiz->esquerda, valor);
    } else {
        raiz->direita = inserir(raiz->direita, valor);
    }
    return raiz;
}

// Função para encontrar o menor valor de um nó
No* menorValor(No* raiz) {
    No* atual = raiz;
    while (atual && atual->esquerda != NULL) {
        atual = atual->esquerda;
    }
    return atual;
}

// Função para remover um nó da árvore
No* remover(No* raiz, int valor) {
    if (raiz == NULL) {
        return raiz;
    }
    if (valor < raiz->valor) {
        raiz->esquerda = remover(raiz->esquerda, valor);
    } else if (valor > raiz->valor) {
        raiz->direita = remover(raiz->direita, valor);
    } else {
        if (raiz->esquerda == NULL) {
            No* temp = raiz->direita;
            free(raiz);
            return temp;
        } else if (raiz->direita == NULL) {
            No* temp = raiz->esquerda;
            free(raiz);
            return temp;
        }
        No* temp = menorValor(raiz->direita);
        raiz->valor = temp->valor;
        raiz->direita = remover(raiz->direita, temp->valor);
    }
    return raiz;
}

// Função para exibir a árvore organizada
void exibir(No* raiz, int espaco) {
    if (raiz == NULL) return;
    espaco += 5;
    exibir(raiz->direita, espaco);
    printf("\n");
    for (int i = 5; i < espaco; i++)
        printf(" ");
    printf("%d\n", raiz->valor);
    exibir(raiz->esquerda, espaco);
}

// Função para liberar a memória da árvore
void liberarArvore(No* raiz) {
    if (raiz != NULL) {
        liberarArvore(raiz->esquerda);
        liberarArvore(raiz->direita);
        free(raiz);
    }
}

int main() {
    No* raiz = NULL;
    int valores[] = {50, 75, 25, 85, 65, 35, 15, 90, 80, 70, 60, 40, 30, 20, 10};
    int tamanho = sizeof(valores) / sizeof(valores[0]); // Pequeno truque para achar tamanho.

    for (int i = 0; i < tamanho; i++) {
        raiz = inserir(raiz, valores[i]);
    }

    printf("Arvore Binaria:\n");
    exibir(raiz, 0);

    liberarArvore(raiz);
    return 0;
}
