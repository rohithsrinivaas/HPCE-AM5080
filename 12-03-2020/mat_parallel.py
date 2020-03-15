import math
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
import numpy as np
import random

np.set_printoptions(precision = 3)
np.set_printoptions(suppress = True)

if rank == 0 :
	A = np.random.rand(12,4)
	B = np.random.rand(4,6)
	if(A.ndim != 2 or B.ndim != 2):
		print("Error, more that 2 dimensions \n")
	rows = np.shape(A)[0]
	cols = np.shape(B)[1]
	k = np.shape(A)[1]
	print(rows)
	print(cols)
	print(k)
	for i in range(size):
		comm.send(rows, dest = i)
		comm.send(cols, dest = i)

rows = comm.recv(source = 0)
cols = comm.recv(source = 0)
iprocs = 6
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
prod = np.dot(r,c)
print(rank, prod)
comm.send(prod, dest = 0)
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
	print(C)
if rank == 0:
	print(np.dot(A,B))
