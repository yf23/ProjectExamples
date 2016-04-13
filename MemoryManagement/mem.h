/* 
 * CSE 374 HW6
 * Yu Fu, Yue Liu
 * Mar 5, 2015
 *
 * mem.h - Interface to Memory Management Package
 */

#ifndef MEM_H
#define MEM_H

#include <stdio.h>
#include <inttypes.h>

/*
 * Return a pointer to a new block of storage 
 * aligned on a 16-byte boundary.
 * The block has at least given size bytes of memory.
 * If given size less or equal than 0, return NULL. 
 */
void* getmem(uintptr_t size);

/*
 * Return the block of storage at given location p 
 * to the pool of available free storage. 
 * If p is NULL, freemem has no effect.
 * Also combine adjacent free memory blocks into
 * one larger block.
 */
void freemem(void* p);

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
void get_mem_stats(uintptr_t* total_size, uintptr_t* total_free, uintptr_t* n_free_blocks);

/*
 * Print a formatted listing on file f showing the 
 * blocks on the free list.
 * Each line contains the block's address and length.
 */
void print_heap(FILE * f);

#endif /* ifndef MEM_H */
