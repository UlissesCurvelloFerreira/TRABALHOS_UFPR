// Ulisses Curvello Ferreira
// GRR: 20223829

#include "lu.h"

/* Realiza a fatoração LU para matriz tridiagonal
 * Armazena os multiplicadores diretamente na estrutura tridiagonal*/
void fatoraLU(Tridiag *sl)
{
  // A diagonal principal de L é sempre 1 (implícito)
  // A diagonal principal de U é igual à diagonal principal do sistema
  // A diagonal superior de U é igual à diagonal superior do sistema
  
  // Precisamos calcular apenas os multiplicadores (diagonal inferior de L)
  for (int i = 1; i < sl->n; i++) {
    sl->Di[i] /= sl->D[i-1];              // Calcula o multiplicador e armazena na diagonal inferior
    sl->D[i] -= sl->Di[i] * sl->Ds[i-1];  // Atualiza a diagonal principal usando o multiplicador
  }
}


/* Resolve o sistema Ly = b, onde L é a matriz triangular inferior
 * Os multiplicadores estão armazenados em sl->Di*/
void resolveL(Tridiag *sl, real_t *y)
{
  y[0] = sl->B[0];               // Primeiro elemento
  
  for (int i = 1; i < sl->n; i++) {
    y[i] = sl->B[i] - sl->Di[i] * y[i-1];
  }
}


/* Resolve o sistema Ux = y, onde U é a matriz triangular superior
 * A diagonal principal está em sl->D e a diagonal superior em sl->Ds*/
void resolveU(Tridiag *sl, real_t *y, real_t *x)
{
  int n = sl->n;                  // Mais fácil de colocar as contas;
  x[n-1] = y[n-1] / sl->D[n-1];   // Último elemento
  
  for (int i = n-2; i >= 0; i--) {
    x[i] = (y[i] - sl->Ds[i] * x[i+1]) / sl->D[i];
  }
}

/* Imprime cada elemento de x com 15 casas decimais */
void imprimeSolucao(real_t *x, int n)
{
    printf("\n");
    for (int i = 0; i < n; i++) {
        printf(" %23.15e", x[i]);
    }
    printf("\n");
}
