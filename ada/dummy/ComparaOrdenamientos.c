/**
 * ComparaOrdenamientos.c
 * ========================
 *
 *
 * Descripcion:
 * ------------
 * Compara bubble sort contra quick sort sobre arreglos aleatorios de
 * 2^1 hasta 2^25 elementos. Por cada tamano y algoritmo anota una
 * linea "n,segundos" en un .txt propio, listo para graficarse.
 *
 *
 * Considerations:
 * ------------
 * - Compilar con:
 *   gcc -O2 -Wall -Wextra -o ComparaOrdenamientos ComparaOrdenamientos.c
 * - La burbuja es O(n^2): con 2^25 elementos tardaria alrededor de dos
 *   semanas, asi que por defecto solo corre hasta 2^EXP_MAX_BURBUJA.
 *   El primer argumento opcional cambia ese tope sin recompilar:
 *   ./ComparaOrdenamientos 20
 * - La semilla es fija para que ambos algoritmos ordenen exactamente
 *   los mismos arreglos y las corridas sean reproducibles
 * - La copia del arreglo y la verificacion quedan fuera del cronometro;
 *   solo se mide el ordenamiento puro
 *
 *
 * Metadata:
 * ----------
 * * Author: zxxz6 (Bryan Violante Arriaga)
 * * Version: 1.0.0
 *
 *
 * History:
 * ------------
 * Author      Date            Description
 * zxxz6       20/08/2026      Creation
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* Rango de tamanos: 2^EXP_MIN hasta 2^EXP_MAX elementos */
#define EXP_MIN 1
#define EXP_MAX 25

/* Tope por defecto de la burbuja; 2^18 ya tarda del orden de un
 * minuto y cada exponente extra multiplica el tiempo por cuatro */
#define EXP_MAX_BURBUJA 18

/* Semilla fija: misma entrada en cada corrida y para cada algoritmo */
#define SEMILLA 20260820

#define ARCHIVO_BURBUJA "TiemposBurbuja.txt"
#define ARCHIVO_QUICK   "TiemposQuick.txt"

/**
 * Intercambia el contenido de dos posiciones enteras.
 * Con -O2 el compilador la inserta en el lugar, asi que usarla desde
 * los ciclos internos no cuesta una llamada real.
 *
 * Inputs:
 * -------
 * a: Puntero al primer entero
 * b: Puntero al segundo entero
 *
 * Returns:
 * -------
 * void
 *
 */
static void intercambiar(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

/**
 * Llena el arreglo con enteros pseudoaleatorios de rand().
 * No siembra la semilla; el llamador llama srand() una sola vez al
 * inicio para que toda la corrida sea reproducible.
 *
 * Inputs:
 * -------
 * arr: Arreglo destino, ya reservado con al menos n posiciones
 * n: Cantidad de elementos a generar
 *
 * Returns:
 * -------
 * void
 *
 */
static void llenar_aleatorio(int *arr, size_t n)
{
    for (size_t i = 0; i < n; i++) {
        arr[i] = rand();
    }
}

/**
 * Ordena el arreglo ascendente con bubble sort en su version simple.
 * Recorre los dos ciclos anidados completos, sin bandera de salida
 * temprana, igual que la version analizada en clase: mejor, promedio
 * y peor caso cuestan lo mismo, O(n^2).
 *
 * Inputs:
 * -------
 * arr: Arreglo a ordenar, se modifica en el lugar
 * n: Cantidad de elementos
 *
 * Returns:
 * -------
 * void
 *
 */
static void ordenar_burbuja(int *arr, size_t n)
{
    for (size_t i = 0; i + 1 < n; i++) {
        for (size_t j = 0; j + 1 < n - i; j++) {
            if (arr[j] > arr[j + 1]) {
                intercambiar(&arr[j], &arr[j + 1]);
            }
        }
    }
}

/**
 * Ordena el segmento arr[izq..der] ascendente con quick sort.
 * Toma el elemento de en medio como pivote y particiona con el
 * esquema de Lomuto; con entrada aleatoria la recursion queda en
 * O(log n) niveles esperados.
 *
 * Inputs:
 * -------
 * arr: Arreglo a ordenar, se modifica en el lugar
 * izq: Indice inferior del segmento, inclusivo
 * der: Indice superior del segmento, inclusivo
 *
 * Returns:
 * -------
 * void
 *
 */
static void ordenar_quick(int *arr, long izq, long der)
{
    if (izq >= der) {
        return;
    }

    long medio = izq + (der - izq) / 2;
    intercambiar(&arr[medio], &arr[der]);

    int pivote = arr[der];
    long i = izq - 1;
    for (long j = izq; j < der; j++) {
        if (arr[j] <= pivote) {
            i++;
            intercambiar(&arr[i], &arr[j]);
        }
    }
    i++;
    intercambiar(&arr[i], &arr[der]);

    ordenar_quick(arr, izq, i - 1);
    ordenar_quick(arr, i + 1, der);
}

/**
 * Verifica que el arreglo quedo en orden ascendente.
 * Es el paso de verificacion visto en clase: ordenar es una cosa y
 * comprobar que el resultado es valido es un paso aparte.
 *
 * Inputs:
 * -------
 * arr: Arreglo a revisar
 * n: Cantidad de elementos
 *
 * Returns:
 * -------
 * int: 1 si esta ordenado, 0 si hay algun par en desorden
 *
 */
static int esta_ordenado(const int *arr, size_t n)
{
    for (size_t i = 0; i + 1 < n; i++) {
        if (arr[i] > arr[i + 1]) {
            return 0;
        }
    }
    return 1;
}

/**
 * Calcula los segundos transcurridos entre dos instantes.
 * Los instantes vienen de clock_gettime con CLOCK_MONOTONIC, que no
 * brinca si el sistema ajusta la hora a mitad de la medicion.
 *
 * Inputs:
 * -------
 * ini: Instante inicial
 * fin: Instante final
 *
 * Returns:
 * -------
 * double: Diferencia fin menos ini en segundos, con fraccion
 *
 */
static double segundos_entre(struct timespec ini, struct timespec fin)
{
    return (double)(fin.tv_sec - ini.tv_sec)
         + (double)(fin.tv_nsec - ini.tv_nsec) / 1e9;
}

/**
 * Copia el arreglo base, lo ordena con el algoritmo pedido y mide el
 * tiempo del ordenamiento puro.
 * La copia y la verificacion quedan fuera del cronometro. Si el
 * resultado no queda ordenado el programa aborta: el tiempo de un
 * algoritmo incorrecto no sirve de nada.
 *
 * Inputs:
 * -------
 * usar_quick: 1 para quick sort, 0 para bubble sort
 * base: Arreglo original, no se modifica
 * trabajo: Arreglo auxiliar del mismo tamano, se sobreescribe
 * n: Cantidad de elementos
 *
 * Returns:
 * -------
 * double: Segundos que tardo el ordenamiento
 *
 */
static double medir(int usar_quick, const int *base, int *trabajo,
                    size_t n)
{
    struct timespec ini;
    struct timespec fin;

    memcpy(trabajo, base, n * sizeof(int));

    clock_gettime(CLOCK_MONOTONIC, &ini);
    if (usar_quick) {
        ordenar_quick(trabajo, 0, (long)n - 1);
    } else {
        ordenar_burbuja(trabajo, n);
    }
    clock_gettime(CLOCK_MONOTONIC, &fin);

    if (!esta_ordenado(trabajo, n)) {
        fprintf(stderr,
                "ERROR: el resultado no quedo ordenado (n=%zu, "
                "quick=%d)\n", n, usar_quick);
        exit(EXIT_FAILURE);
    }
    return segundos_entre(ini, fin);
}

/**
 * Corre el experimento completo y escribe los dos archivos de salida.
 * Para cada n = 2^EXP_MIN ... 2^EXP_MAX genera un arreglo aleatorio,
 * lo ordena con cada algoritmo y anota "n,segundos" en el .txt que le
 * toca. La burbuja se corta en el tope para que la corrida termine en
 * minutos y no en semanas.
 *
 * Inputs:
 * -------
 * argc: Cantidad de argumentos de linea de comandos
 * argv: argv[1] opcional, exponente tope para la burbuja
 *
 * Returns:
 * -------
 * int: EXIT_SUCCESS si todo corrio, EXIT_FAILURE ante cualquier falla
 *
 */
int main(int argc, char *argv[])
{
    int tope_burbuja = EXP_MAX_BURBUJA;
    if (argc > 1) {
        tope_burbuja = atoi(argv[1]);
        if (tope_burbuja < EXP_MIN || tope_burbuja > EXP_MAX) {
            fprintf(stderr, "Uso: %s [tope_burbuja entre %d y %d]\n",
                    argv[0], EXP_MIN, EXP_MAX);
            return EXIT_FAILURE;
        }
    }

    size_t n_max = (size_t)1 << EXP_MAX;
    int *base = malloc(n_max * sizeof(int));
    int *trabajo = malloc(n_max * sizeof(int));
    if (base == NULL || trabajo == NULL) {
        fprintf(stderr, "ERROR: sin memoria para %zu enteros\n",
                n_max);
        free(base);
        free(trabajo);
        return EXIT_FAILURE;
    }

    FILE *f_burbuja = fopen(ARCHIVO_BURBUJA, "w");
    FILE *f_quick = fopen(ARCHIVO_QUICK, "w");
    if (f_burbuja == NULL || f_quick == NULL) {
        fprintf(stderr, "ERROR: no pude abrir %s o %s\n",
                ARCHIVO_BURBUJA, ARCHIVO_QUICK);
        free(base);
        free(trabajo);
        return EXIT_FAILURE;
    }
    fprintf(f_burbuja, "n,segundos\n");
    fprintf(f_quick, "n,segundos\n");

    srand(SEMILLA);
    for (int exp = EXP_MIN; exp <= EXP_MAX; exp++) {
        size_t n = (size_t)1 << exp;
        llenar_aleatorio(base, n);

        double t_quick = medir(1, base, trabajo, n);
        fprintf(f_quick, "%zu,%.9f\n", n, t_quick);
        fflush(f_quick);

        if (exp <= tope_burbuja) {
            double t_burbuja = medir(0, base, trabajo, n);
            fprintf(f_burbuja, "%zu,%.9f\n", n, t_burbuja);
            fflush(f_burbuja);
            printf("2^%-2d n=%-9zu quick=%11.6f s  "
                   "burbuja=%11.6f s\n", exp, n, t_quick, t_burbuja);
        } else {
            printf("2^%-2d n=%-9zu quick=%11.6f s  "
                   "burbuja=omitida\n", exp, n, t_quick);
        }
        fflush(stdout);
    }

    fclose(f_burbuja);
    fclose(f_quick);
    free(base);
    free(trabajo);

    printf("Listo: %s y %s\n", ARCHIVO_BURBUJA, ARCHIVO_QUICK);
    return EXIT_SUCCESS;
}

//###################### END OF COMPARAORDENAMIENTOS.C #########################
//##############################################################################
