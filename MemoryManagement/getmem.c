/* CSE 374 HW6
   Yu Fu, Yue Liu
   Feb 24, 2015
*/

#include "mem.h"
#include "mem_impl.h"

struct Header base;
struct Header* freelist = NULL;
uintptr_t mem_managed = 0;

/*
 * Return a pointer to a new block of storage 
 * aligned on a 16-byte boundary.
 * The block has at least given size bytes of memory.
 * If given size less or equal than 0, return NULL. 
 */
void* getmem(uintptr_t size)
{
    uintptr_t reqSize;               /* required size with 16-byte alignment */
    struct Header *p, *prevp;        /* pointers used to loop through the free list */
    uintptr_t mallocSize;            /* size to malloc if needed */
  
    /* Zero or negtive size requests get NULL. */
    if (size <= 0)
    {
        return NULL;
    }

    /* Required size with 16-byte alignment, Header + Data. */
    reqSize = ALIGNMENT * ((size + ALIGNMENT - 1) / ALIGNMENT + 1);
  
    /* If there is no free list yet, initialize a free list with one zero-sized block. */
    if ((prevp = freelist) == NULL)
    {
        base.next = freelist = prevp = &base;         /* Set base as the start of freelist. */
        base.size = 0;                                /* Set initial size as 0. */
    }

    /* Search the free list to find the space of enough for reqSize, return the pointer to data. */
    for (p = prevp->next; ; prevp = p, p = p->next)
    {
        if (p->size >= reqSize)                        /* If space found is big enough, */
        {
            /* If the block is not big enough to split into two blocks. */
            if (p->size <= reqSize + MIN_BLOCK_SIZE)    
            { 
                prevp->next = p->next;                 /* Remove the block from the freelist. */
            }
            else                                       /* If the block is too big, split the block, the right block is with reqSize. */
            {
                p->size = p->size - reqSize;           /* Change the size of the left block. */
                p = p + (p->size / ALIGNMENT);         /* Move the pointer to the right block. */
                p->size = reqSize;                     /* Change the size of the right block. */
            }
            freelist = prevp;                          /* Relocate the start of free list, next search will start here. (Extra Credit 1) */
            return (void*)(p + 1);                     /* The result is 16 bytes more than the pointer to Header. RETURN. */
        }

        if (p == freelist)                             /* If reach the end of freelist with no found, grow the freelist. */
        {
            mallocSize = reqSize;                 
            if (reqSize < MIN_MALLOC_SIZE)
            {
                mallocSize = MIN_MALLOC_SIZE;
            }                                          
            p = (struct Header*) malloc(mallocSize);   /* Malloc requested amount bytes, but at least MIN_MALLOC_SIZE bytes of memory. */
            p->size = mallocSize;                      /* Update the size of new block. */
            freemem((void*)(p + 1));                   /* Return this block to freelist for search */
            p = freelist;                              /* Search start from the beginning of freelist, which is the new added block. */
            mem_managed += mallocSize;                 /* Update the size of managed memory */
        }
    }
}
