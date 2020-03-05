from mpi4py import MPI

comm =  MPI.COMM_WORLD
nproc = comm.Get_size()
rank = comm.Get_rank()

print("Hello World from rank " + str(rank) + " of total processors " + str(nproc) + '\n')

comm.barrier()
