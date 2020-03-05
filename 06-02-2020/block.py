from mpi4py import MPI
import numpy as np
n = 100

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
p = comm.Get_size()


t = int(np.ceil(n/p))
if rank < p:
	if rank==0:
		start = MPI.Wtime()
	suming = 0
	for i in range(t*rank+1, 1+min(100,t*(rank+1))):
		suming = suming + i

if rank > 0:
	comm.send(suming, dest=0)
else:
	for j in range(1,p):
		tp = comm.recv(source=j)
		suming = suming + tp
	end = MPI.Wtime()
	print("sum of first "+str(int(n))+" natural numbers is "+str(suming)+" using "+str(p)+" procs")
	print("method : block")
	print("time taken is "+str(end-start))
