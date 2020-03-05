
from mpi4py import MPI
import numpy as np
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
p =  comm.Get_size()
n =  p
no_levels = 1 + math.ceil(math.log2(p));

data = rank + 1

for i in range(no_levels-1):
	if (rank%2**(i+1) == 2**i):
		comm.send(data,dest = rank - 2**i)
	if (rank%2**(i+1) == 0):
		if (rank + 2**i <= p-1):
			data = data + comm.recv(source = rank + 2**i)


if rank == 0:
	print(data)
	












