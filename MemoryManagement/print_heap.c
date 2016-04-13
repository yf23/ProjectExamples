/*
 * CSE 374 HW6
 * Yu Fu, Yue Liu
 * Mar 5, 2015
 *
 * print_heap.c - implementation of function print_heap
 */

#include "mem.h"
#include "mem_impl.h"

/*
 * Print a formatted listing on file f showing the 
 * blocks on the free list.
 * Each line contains the block's address and length.
 */
void print_heap(FILE * f)
{
    if (freelist != NULL)
    {
        int blockCount = 0;
        struct Header *p = freelist;
        fprintf(f, "%p 0x%x\n Block %u", p, (int)p->size, blockCount++);
        p = p->next;                /* Print the first block */
        while (p != freelist)       /* Loop through the free list to print other blocks */
        {
            fprintf(f, "%p 0x%x\n Block %u", p, (int)p->size, blockCount++);
            p = p->next;
        }
        fclose(f);
    }
}
