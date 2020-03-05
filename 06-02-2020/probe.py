from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
	data = rank*np.ones(2,dtype = np.float64)
	comm.Send([data,MPI.DOUBLE],dest = 1, tag= 1)
if rank == 1:
	info = MPI.Status()
	comm.Probe(MPI.ANY_SOURCE, MPI.ANY_TAG, info)
	source = info.Get_source()
	tag = info.Get_tag()
	count = info.Get_elements(MPI.DOUBLE)
	size = info.Get_count()
	print 'on',rank,'source, tag, count, size is', source, tag, count, size

