from mpi4py import MPI
'''
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
	data = {'a':7, 'b':3.14}
	comm.send(data,dest=1,tag=11)
	print "sent"
elif rank == 1:
	data = comm.recv(source=0,tag=11)
	print "received"
	print "displaying..."
	print data
'''

'''
comm =MPI.COMM_WORLD
my_rank = comm.Get_rank()
p = comm.Get_size()

if my_rank != 0:
	msg = "Hello from " + str(my_rank)
	comm.send(msg,dest = 0)
	print my_rank
	print "sending...."
elif my_rank == 0:
	for proc_id in range(1,p):
		print "receiving"
		msg = comm.recv(source = proc_id)
		print "process " + str(my_rank) + "receives msg from process" + str(proc_id) + ":" + msg

'''

'''
n = 4
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
'''


# ring program
n = 4 # 

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
p = comm.Get_size()

# front and back together one round 
count = -1
for i in range(n):
		if rank == 0:
			count = count + 1

			comm.send(count,dest = 1)
			print "data {0} send to process from rank {1}".format(count,rank)

		elif:
			for j in range(1,p-1):
				count = comm.recv(source=j-1)
				print "data {0} received on process with rank {1}".format(count,rank)

				count = count + 1;

				comm.send(count,dest =  j+1)
				print "data {0} send to process from rank {1}".format(count,rank)
		if rank == p-1:
			count = 	comm.recv(	
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

