from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
import sys




def gcd(a,b):
	a = int(a);
	b = int(b);
	if(a == 0): 
		return b; 
	if(b == 0): 
		return a; 
   
	# base case 
	if(a == b): 
        	return a; 
	if (a > b): 
	        return gcd(a-b, b); 
	return gcd(a, b-a); 

def process_id(i,j,nproc_rows,nproc_cols):
	return 0;
	

comm = MPI.COMM_WORLD
nProcs = comm.Get_size() # nProcs = 6;
rank = comm.Get_rank()

rows = int(sys.argv[1]);
inter = int(sys.argv[2]);
cols = int(sys.argv[3]);

if rank == 0:
	A = np.random.randint(5, size=(rows, inter))
	B = np.random.randint(5, size=(inter, cols))
	C = np.zeros((rows,cols))
	print(gcd(rows,cols),)
	r_procs = rows/gcd(rows,cols);
	c_procs = cols/gcd(rows,cols);
