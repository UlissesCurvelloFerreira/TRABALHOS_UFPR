// Ulisses Curvello Ferreira
// GRR: 20223829

#ifndef LU_H
#define LU_H

#include <stdio.h>
#include "utils.h"
#include "edo.h"

// Realiza a fatoração LU do sistema tridiagonal (modifica o próprio sistema)
void fatoraLU(Tridiag *sl);

// Resolve o sistema Ly = b usando substituição direta (L é triangular inferior)
void resolveL(Tridiag *sl, real_t *y);

// Resolve o sistema Ux = y usando substituição reversa (U é triangular superior)
void resolveU(Tridiag *sl, real_t *y, real_t *x);

// Imprime o vetor solução x do sistema linear
void imprimeSolucao(real_t *x, int n);

#endif // __LU_H__
