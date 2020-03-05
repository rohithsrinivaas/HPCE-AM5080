from mpi4py import MPI
import numpy as np
comm = MPI.COMM_WORLD
p = comm.Get_size()
rank = comm.Get_rank()

def fun(x):
	return x**2;

integral = 0
a = 0
b = 1
n = 1024

h = (b-a)/(n)
t = int(np.ceil(n/p))

strip = [];
stripsum = 0;
striparea = 0;
for i in range(t*rank+1, 1+min(n,t*(rank+1))):
	#print(i,rank)
	striparea = (h/2)*( fun(a + (i*h)) + fun(a+ ((i+1)*h)))
	strip.append(striparea)
	stripsum = np.sum(np.array(strip))

integral = comm.reduce(stripsum,MPI.SUM, root = 0)	
	
if rank == 0:
	print(integral)
