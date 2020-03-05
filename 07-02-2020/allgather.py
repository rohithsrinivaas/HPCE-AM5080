from mpi4py import MPI
import numpy as np
 
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

data = np.array([(rank+1)**2, rank])
print("Before")
print(data,rank)
data = np.array(comm.allgather(data))
print("After")
print(data,rank)


