/*
 * CSE 374 HW6
 * Yu Fu, Yue Liu
 * Mar 5, 2015
 *
 * mem_impl.h - the declarations of the free list data structure
 *
 *           ________________________________        ________________...(TO NEXT HEADER)
 *   ________|______________________________|________|_______________...(THE LAST　BLOCK IN LIST WILL POINT BACK TO THE START)
 *  v        |                              v        |          
 *  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 *  |  size  |  *next  |    data   | ...... |  size  |  *next  |    data    | ...
 *  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 *  | HEADER 16 bytes  |    DATA   |
 *    
 */

#ifndef MEM_IMPL_H
#define MEM_IMPL_H

#include <inttypes.h>
#include <stdlib.h>

struct Header                              /* Header structure, takes 16 bytes */
{
    uintptr_t size;                        /* size of this block */
    struct Header *next;                   /* next block on free list */
};

extern struct Header base;                 /* empty list to get started */
extern struct Header *freelist;            /* start of free list */

extern uintptr_t mem_managed;              /* the size of memory has been managed, for report purpose */

#define ALIGNMENT 16                       /* the alignment of the blocks should be the size of Header, which is 16 bytes */
#define MIN_BLOCK_SIZE 32                  /* the minimum size of the block, which is 16(header) + 16(data) = 32 */
#define MIN_MALLOC_SIZE 8192               /* the minimum size for malloc request */

#endif                                     /* MEM_IMPL_H */
