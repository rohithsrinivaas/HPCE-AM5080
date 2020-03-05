from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


suming  = 0
data = (rank+1)**2
suming = comm.reduce(data,MPI.SUM, 0)	
if rank == 0:
	print(suming)
