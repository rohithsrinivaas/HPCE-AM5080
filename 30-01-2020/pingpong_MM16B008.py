from mpi4py import MPI
n = 4 # number of rounds
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# front and back together one round 
count = -1
for i in range(n):
	if not i:
		
		if rank == 0:
			count = count + 1
			comm.send(count,dest = 1)
			print "data {0} send to process from rank {1}".format(count,rank)

		elif rank == 1:
			count = comm.recv(source=0)
			print "data {0} received on process with rank {1}".format(count,rank)
			count = count + 1;
			comm.send(count,dest = 0)
			print "data {0} send to process from rank {1}".format(count,rank)	
	else:	
		if rank == 0:
			count = comm.recv(source = 1)
			print "data {0} received on process with rank {1}".format(count,rank)		
			count = count + 1
			comm.send(count,dest = 1)
			print "data {0} send to process from rank {1}".format(count,rank)	
			
		elif rank == 1:
			count = comm.recv(source=0)
			print "data {0} received on process with rank {1}".format(count,rank)
			count = count + 1; 
			comm.send(count,dest = 0)	
			print "data {0} send to process from rank {1}".format(count,rank)

	comm.barrier()

