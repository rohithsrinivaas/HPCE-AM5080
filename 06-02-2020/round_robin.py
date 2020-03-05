from mpi4py import MPI
import numpy as np

n = 10 # sum from to 1 to n:

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
p = comm.Get_size()

# round robin fashion 

for j in range(1,p):
	if rank == 0:
		overall = 0;		
		arr = [];
		var = 0;
		i= 0;
		while(1):
			var = (p-1)*i + j
			if var > n:
				break
			else:			
				arr.append(var)
				i = i+1
		arr = np.array(arr)
		comm.send(arr,dest=j)
		print(" array in the " + str(j) + " process")
		print(arr)
	if rank == j:
		arr = comm.recv(source = 0)
		comm.send(np.sum(arr),dest=0)
for j in range(1,p):
	if rank ==0:
		overall = overall + comm.recv(source = j)
if rank == 0:
	print("Overall sum is : ")	
	print(overall)

	
