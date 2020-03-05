from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

nxt = (rank+1)%size
prev = (rank-1)%size

if rank == 0:
	data = np.array([0],dtype = 'i')

count  = 0;
while(count < 5):
	if rank !=0:
		data = np.empty([1],dtype = 'i')
		comm.Recv([data,MPI.INT],source= prev, tag= 11)
		print('Count : ', count , data, 'received at',rank,'from',prev)
	comm.Send([data, MPI.INT],dest = nxt,tag = 11)
	print('Count:',count,data,'sent from',rank,'to',nxt)


	if rank == 0:
		comm.Recv([data,MPI.INT],source=prev, tag=11)
		print('Count:',count, data, 'received at', rank,'from',prev)
	count = count + 1;



