/* CSE 374 HW6
 * Yu Fu, Yue Liu
 * Mar 5, 2015
 *
 * freemem.c - implementation of function freemem.
 */

#include "mem.h"
#include "mem_impl.h"

/*
 * Return the block of storage at given location p 
 * to the pool of available free storage. 
 * If p is NULL, freemem has no effect.
 * Also combine adjacent free memory blocks into
 * one larger block.
 */

void freemem(void* p)
{   
    /* No effect if p is NULL */
    if (p == NULL)
    {
        return;
    }

    struct Header *headerOfBlock = (struct Header *)p - 1;    /* pointer to block header */
    struct Header *ptr;                                       /* pointer to visit freelist */

    /* Loop through the freelist to find a place the put free block */
    /* Break the for loop if find a place in the list */
    for (ptr = freelist; !(headerOfBlock > ptr && headerOfBlock < ptr->next); ptr = ptr->next)
    {
        if (ptr == headerOfBlock)
        {
            return;
        }
        
        if (ptr >= ptr->next                                  /* reach the end of freelist */
            && (headerOfBlock > ptr                           /* new block should be at end of freelist */
            ||  headerOfBlock < ptr->next))                   /* new block should be at a start of freelist */
        {
            break;
        }
    }
    /* ptr stops at the block previous the place to put given free block,
       or the last node of free list. */ 

    if (headerOfBlock + headerOfBlock->size == ptr->next)     /* When given free block is adjacent to another free block on the right side */
    {
        headerOfBlock->size += ptr->next->size;               /* Combine the size of two blocks */
        headerOfBlock->next = ptr->next->next;                /* Only keep the header of given free block */
    }
    else                                                      /* not adjacent */
    {
        headerOfBlock->next = ptr->next;                      /* Connect the given free block with right neighbor in the list */
    }

    if (ptr + ptr->size == headerOfBlock)                     /* When given free block is adjacent to another free block on the left side */
    {
        ptr->size += headerOfBlock->size;                     /* Combine the size of two blocks */
        ptr->next = headerOfBlock->next;                      /* Only keep the the header of left adjacent block */
    }
    else                                                      /* not adjacent */
    {
        ptr->next = headerOfBlock;                            /* Connect the given free block with left neighbor in the list */
    }
    freelist = ptr;                                           /* Let the free list start at the new adding block */
}
