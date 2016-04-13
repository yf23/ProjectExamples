/*
 * CSE 374 HW6
 * Yu Fu, Yue Liu
 * Mar 5, 2015
 *
 * get_mem_stats.c - implementation of function get_mem_stats 
 */

#include "mem.h"
#include "mem_impl.h"

/*
 * Store statistics about current state of the 
 * memory manager in the three given integer varaibles.
 * total_size: total amount of storage in bytes 
 *             acquired by the memory manager
 * total_free: total amount of storage in bytes 
 *             stored on the free list
 * n_free_blocks: total number of individual blocks
 *                currently stored on the free list
 */

void get_mem_stats(uintptr_t* total_size, uintptr_t* total_free, uintptr_t* n_free_blocks)
{
    *total_size = mem_managed;      /* Get size of total amount of storage from global variable. */
    *total_free = 0;           
    *n_free_blocks = 0;
    if (freelist != NULL)           /* Check if there is a free block list. */
    {   
        struct Header *p = freelist;
        
        if (p->size != 0)           /* Skip size = 0 block which is initially base. */
        {
            *total_free = p->size;
            *n_free_blocks = 1; 
        }
        
        p = p->next;                /* Add the first block of free list to the stats. */
        while (p != freelist)       /* Loop through the free list to add other blocks to the stats. */
        {   
            if (p->size != 0)       /* Skip size = 0 block which is initially base. */
            {
                *total_free += p->size;
                *n_free_blocks += 1;
            }
            p = p->next;
        }
    }
}

