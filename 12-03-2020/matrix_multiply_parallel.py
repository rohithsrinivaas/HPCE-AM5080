import math
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nProcs = comm.Get_size()
import numpy as np
import random


def gcd(x, y): 
   while(y): 
       x, y = y, x % y 
  
   return x 

if rank == 0 :
	A = np.random.rand(4,3)
	B = np.random.rand(3,6)
	rows = np.shape(A)[0]
	cols = np.shape(B)[1]
	print(gcd(rows,cols))
	k = np.shape(A)[1]
	#Sending the shape of the array to different processors
	for i in range(nProcs):
		comm.send(rows, dest = i)
		comm.send(cols, dest = i)

rows = comm.recv(source = 0)
cols = comm.recv(source = 0)
iprocs = 2
jprocs = 3
iLength = int(rows/iprocs)
jLength = int(cols/jprocs)

if rank == 0:
	for i in range(iprocs):
		for j in range(jprocs):
			r = A[i*iLength:(i+1)*iLength,:]
			c = B[:,j*jLength:(j+1)*jLength]
			comm.send(r,dest = i*jprocs+j, tag = 0)
			comm.send(c,dest = i*jprocs+j, tag = 1)
r = comm.recv(source = 0, tag = 0)
c = comm.recv(source = 0, tag = 1)
comm.barrier()
result = np.dot(r,c)
comm.send(result, dest = 0)
if rank == 0:
	for i in range(iprocs):
		for j in range(jprocs):
			mat = comm.recv(source = i*jprocs+j)
			if j == 0:
				row = mat
			else:
				row = np.hstack((row, mat))
		if i == 0:
			C = row
		else:
			C = np.vstack((C,row))
	print("matrix multiplication thru MPI")		
	print(C)
if rank == 0:
	print("matrix multiplication thru numpy function")
	print(np.dot(A,B))
