// Ulisses Curvello Ferreira
// GRR: 20223829

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <fenv.h>
#include <likwid.h>

#include "utils.h"
#include "edo.h"
#include "lu.h"


int main()
{
  LIKWID_MARKER_INIT;


  fesetround(FE_DOWNWARD);

  EDo edo;
  int edo_count;
  
  scanf("%d", &edo.n);                   // 1ª linha: quantidade de pontos da malha da EDO;
  scanf("%lf %lf", &edo.a, &edo.b);      // 2ª linha: intervalo a e b onde a EDO é válida;
  scanf("%lf %lf", &edo.ya, &edo.yb);    // 3ª linha: os valores de contorno  y(a) e y(b);
  scanf("%lf %lf", &edo.p, &edo.q);      // 4ª linha: os coeficientes p e q da EDO genérica;
  
  
  // Vetores para solução do sistema
  real_t *y = (real_t *)malloc(edo.n * sizeof(real_t));
  real_t *x = (real_t *)malloc(edo.n * sizeof(real_t));
  
  // Para cada conjunto de coeficientes r1, r2, r3, r4
  edo_count = 0;
  while (scanf("%lf %lf %lf %lf", &edo.r1, &edo.r2, &edo.r3, &edo.r4) == 4) {
    edo_count++;
    
    Tridiag *sl = genTridiag(&edo);     // Função do professor que Gera o sistema tridiagonal;
    prnEDOsl(&edo);                     // Função do professor que Imprime o tridiagonal;
    

    rtime_t start_time = timestamp();
  
    LIKWID_MARKER_START("LU_FATORACAO");
    fatoraLU(sl);
    LIKWID_MARKER_STOP("LU_FATORACAO");

    
    string_t resolve = markerName("RESOLVE_LU", edo_count);
    LIKWID_MARKER_START(resolve);              
    resolveL(sl, y);              
    resolveU(sl, y, x);
    LIKWID_MARKER_STOP(resolve);       
    
    rtime_t elapsed_time = timestamp() - start_time;
    free(resolve);

    imprimeSolucao(x, edo.n);
    printf(" %.8e\n\n", elapsed_time);   // Imprime tempo gasto
    
    // Libera memória do sistema linear
    free(sl->D);
    free(sl->Di);
    free(sl->Ds);
    free(sl->B);
    free(sl);
  }

  free(y);
  free(x);
  LIKWID_MARKER_CLOSE;

  return 0;
}