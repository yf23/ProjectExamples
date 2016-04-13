# Makefile for Memory Management
# CSE 374 HW6
# Yu Fu, Yue Liu
# Mar 5, 2015

# default target bench, generate the bench executable program
bench: bench.o getmem.o freemem.o get_mem_stats.o print_heap.o
	gcc -Wall -std=c11 -g -o bench bench.o getmem.o freemem.o get_mem_stats.o print_heap.o

# individual source files
bench.o: bench.c mem.h mem_impl.h
	gcc -Wall -std=c11 -g -c bench.c

getmem.o: getmem.c mem.h mem_impl.h
	gcc -Wall -std=c11 -g -c getmem.c

freemem.o: freemem.c mem.h mem_impl.h
	gcc -Wall -std=c11 -g -c freemem.c

get_mem_stats.o: get_mem_stats.c mem.h mem_impl.h
	gcc -Wall -std=c11 -g -c get_mem_stats.c

print_heap.o: print_heap.c mem.h mem_impl.h
	gcc -Wall -std=c11 -g -c print_heap.c

# test, run the bench with default program
test:
	make bench
	./bench
# dist, create an archive named hw6.tar containing all the files
dist:
	make clean
	git log >git.log
	tar cvf hw6.tar *
	rm git.log
	
# clean, remove any .o files, executables, emacs backup files(*~)
#        and any other files generated as making the program.
clean:
	rm -f *.o bench *~ *.tar *.log \#*

