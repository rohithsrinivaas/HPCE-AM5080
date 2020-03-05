from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

data = np.array([(rank+1)**2,rank])
print(data)
data = np.array(comm.gather(data,root=0))
'''
print(data,rank)
if rank == 0:
	for i in range(size):
		assert data[i] == (i+1)**2
else:
	assert data is None
'''
if rank == 0:
	print(data)
'''
if rank == 1:
	print(data)
'''


