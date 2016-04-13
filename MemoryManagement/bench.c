/* 
 * CSE 374 HW6
 * Yu Fu, Yue Liu
 * Mar 5, 2015
 *
 * bench.c
 * Execute a large number of calls to functions getmem and freemem 
 * to allocate and free blocks of random sizes and in random order.
 * Print the following statistics to stdout 10 times during execution:
 * 1. Total CPU time used by the benchmark test in seconds.
 * 2. Total amount of storage acquired from the underlying system 
 *    by the memory manager.
 * 3. Total number of blocks on the free storage list.
 * 4. Average number of bytes in the free storage blocks.
 * 
 * bench [ntrials [pctget [pctlarge [small_limit [large_limit [random_seed ]]]]]]
 * 
 * ntrials: total number of getmem plus freemem calls. Default 10000.
 * pctget: percent of the total getmem/freemem calls that should be getmem. Default 50.
 * pctlarge: percent of the getmem calls that should request "large" blocks with a size greater than small_limit. Default 10.
 * small_limit: largest size in bytes of a "small" block. Default 200.
 * large_limit: largest size in bytes of a "large" block. Default 20000.
 * random_seed: initial seed value for the random number generator. Default: the system time-of-day clock.
 */

#include "mem.h"
#include "mem_impl.h"
#include <stdio.h>
#include <time.h>

int main(int argc, char** argv)
{
    clock_t   start_t, end_t;
    double    total_t;
    uintptr_t total_size = 0;
    uintptr_t total_free = 0; 
    uintptr_t n_free_blocks = 0;
    uintptr_t ave_bytes_per_block = 0;

    int params[6] = {10000, 50, 10, 200,                        /* Put default values in parameter array. */
                     20000, (int)time(NULL)};    
    
    if (argc > 7)                                               /* Only consider at most 6 parameters. */
    {
        argc = 7;
    }

    
    for (int i = 1; i < argc; i++)                              /* Update parameter array with input value. */
    {
        params[i-1] = atoi(argv[i]); 
    }

    int ntrials = params[0];                                    /* Assign parameters */
    int pctget = params[1];
    int pctlarge = params[2];
    int small_limit = params[3];
    int large_limit = params[4];
    int random_seed = params[5];
    
    void **memblock_list = malloc(sizeof(void *) * ntrials);    /* Array of pointers got by getmem but not freed yet. */
    int list_size = 0;                                          /* Size of the list of memory block pointers. */

    int report_gap = (int) (0.1 * ntrials);                     /* Numbers of trials between each report. */
    int report_number = report_gap;                             /* Numbers of trials needed for next report. */

    start_t  = clock();                                         /* Start recording the time. */
    srand(random_seed);                                         /* Set random seed. */

    for (int i = 0; i < ntrials; i++)
    {
        int freeOrGet = 0;                                      /* 0 is freemem; 1 is getmem. */
        int r_freeOrGet = rand() % 100;                         /* Create a random number from 0 to 99. */
        if (r_freeOrGet < pctget)
        { 
            freeOrGet = 1;                                      /* Make it pctget percent chance to getmem. */
        }

        if (freeOrGet == 1)                                     /* Choose to call getmem. */
        {
            int smallOrLarge = 0;                               /* 0 is to get a small block; 1 is to get a large block. */
            int r_smallOrLarge = rand() % 100;                  /* Create a random number from 0 to 99. */
            if (r_smallOrLarge < pctlarge)
            {
                smallOrLarge = 1;                               /* Make it getLarge percent chance to get a large block. */
            }

            int randSize;                                       /* Size of random block. */
            if (smallOrLarge == 1)                              /* Get a large block with size between small_limit and large_limit. */
            {
                randSize = rand() % (large_limit - small_limit) + small_limit;
            }
            else                                                /* Get a small block with size between 1 and small_limit. */
            {
                randSize = rand() % small_limit + 1;    
            }

            /* Call getmem to get randSize bytes of memory. Put the returned pointer into the list and update the size of list. */
            memblock_list[list_size] = getmem((uintptr_t)randSize);
            list_size = list_size + 1;       
        }
        else if (freeOrGet == 0 && list_size > 0)               /* Choose to call freemem and the list is not empty. */
        {
            int r_b = rand() % list_size;                       /* Randomly choose a valid index from list. */
            freemem(memblock_list[r_b]);                        /* Free the chosen pointer. */
            memblock_list[r_b] = memblock_list[list_size - 1];  /* Move the last pointer in the list to fill in the empty space. */
            list_size = list_size - 1;                          /* Decrease size of the list. */
        }

        if (i == report_number - 1)                             /* Report after every 10% of total calls executed. */
        {
            get_mem_stats(&total_size, &total_free, &n_free_blocks);
            end_t = clock();
            total_t = (double)(end_t - start_t) / CLOCKS_PER_SEC;

            if (n_free_blocks > 0)                              /* Avoid divide 0 error. */
            {
            	ave_bytes_per_block = total_free / n_free_blocks;
            }
            else
            {
            	ave_bytes_per_block = 0;
            }

            printf("Total CPU time used by the benchmark test (seconds):    %.6f\n", total_t);
            printf("Total amount of storage acquired by the memory manager: %lu\n", total_size);
            printf("Total number of blocks on the free storage list:        %lu\n", n_free_blocks);
            printf("Average number of bytes in the free storage blocks:     %lu\n\n", ave_bytes_per_block);

            report_number += report_gap;
        }
    }

    free(memblock_list);                                        /* Free the list of memory block pointers. */
    return 0;
}
