from mpi4py import MPI
import numpy as np
n = 100

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
p = comm.Get_size()

suming  = 0
t = int(np.ceil(n/p))

arr = []
for i in range(t*rank+1, 1+min(100,t*(rank+1))):
	arr.append(i)
	data = np.sum(np.array(arr))
	
suming = comm.reduce(data,MPI.SUM, 0)	
if rank == 0:
	print(suming)

