from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
p = comm.Get_size()
rank = comm.Get_rank()

arr =  np.random.randint(low = 0, high =  40, size = 2*p)
print(arr)
swap = 0
count  = 0


if rank == 0:
	if count%2 == 0:	
		arr = np.reshape(arr,(p,2))

	else:
		arr = np.reshape(
	
pair = comm.scatter(arr, root = 0)
for i in range(p):
	if rank == i:
		if(pair[0] > pair[1]):
			temp =  pair[0]
			pair[0] = pair[1]
			pair[1] = temp

arr = np.array(comm.gather(pair, root =  0))

if rank == 0:
	arr = arr.flatten()
	print(arr)
