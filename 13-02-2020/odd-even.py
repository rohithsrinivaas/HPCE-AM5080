from mpi4py import MPI
import numpy
comm = MPI.COMM_WORLD
p = comm.Get_size()
r = comm.Get_rank()
n = 10
if r==0:
	print("array length : "+str(n))

if p>=(n/2):
	if r < p:
		a = numpy.random.randint(0, 40, size=2)
	comm.barrier()
	arr = numpy.array(comm.gather(a, root=0))
	if r==0:
		arrp = arr.flatten()
		arrp = arrp[0:n]
		print(arrp)
	ns = 1
	c = 0
	while ns > 0:
		ns = 0
		c = c + 1
		if (c%2) != 0:
			if r < n/2:
				if a[0] > a[1]:
					ns = ns + 1
					t = a[0]
					a[0] = a[1]
					a[1] = t
			comm.barrier()
		else:
			if r < n/2:
				if r > 0:
					comm.send(a[0],dest=r-1)
					a[0] = comm.recv(source=r-1)
				if r < n/2 - 1:
					tc = comm.recv(source=r+1)
					if a[1] > tc:
						ns = ns + 1
						t = tc
						tc = a[1]
						a[1] = t
					comm.send(tc,dest=r+1)
			comm.barrier()
		ns = comm.reduce(ns,MPI.SUM, 0)	
		ns = comm.bcast(ns,root=0)
		comm.barrier()
		arr = numpy.array(comm.gather(a, root=0))
		if r==0:
			arrp = arr.flatten()
			arrp = arrp[0:n]
			print(arrp)
