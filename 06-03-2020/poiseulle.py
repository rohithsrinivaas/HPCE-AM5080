#Poiseulle flow simulation
from mpi4py import MPI
import numpy as np
import csv
import matplotlib.pyplot as plt
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nproc = comm.Get_size()

dely = 0.01
L = 1.0
N = int(L/dely*0.5);	#exploiting symmetry about centerline
dom_size = (N+1)/nproc
p_grad = -1.0
mu = 1.0
u = np.zeros(dom_size)
u[:] = 0
if rank == nproc-1:
	u = np.append(u,np.zeros(N + 1 - dom_size*nproc))
	dom_size = dom_size + (N + 1 - dom_size*nproc)

relerr = 1
total_relerr = 1
tol = 1e-4;
urecv = np.empty(1, dtype = np.float64)

unew = np.copy(u)	
breakflag = False
starttime = MPI.Wtime()
while breakflag == False:	
	for i in range(0,dom_size):	
		if i == 0 and rank != 0:
			comm.Send([u[0],MPI.DOUBLE],dest = rank - 1,tag = 1)
			comm.Recv(urecv,source = rank-1,tag = 2)
			unew[i] = (urecv + u[i+1])/2  - (p_grad*dely*dely)/(2*mu)
		if i == dom_size-1 and rank != nproc-1:
			comm.Send([u[-1],MPI.DOUBLE],dest = rank + 1,tag = 2)		
			comm.Recv(urecv,source = rank + 1,tag = 1)	
			unew[i] = (u[i-1] + urecv)/2 - (p_grad*dely*dely)/(2*mu)
		if i == dom_size-1 and rank == nproc - 1:
			unew[i] = (u[i-1] + u[i])/2 - (p_grad*dely*dely)/(2*mu)			
		if i != dom_size-1 and i != 0:
			unew[i] = (u[i-1] + u[i+1])/2 - (p_grad*dely*dely)/(2*mu)
	comm.barrier()
	relerr = sum(np.absolute(unew - u)) #L1 error
	u = np.copy(unew)
	u_final = comm.gather(u, root = 0)
	total_relerr = comm.reduce(relerr,op = MPI.SUM,root = 0)
	if rank == 0:
		u_final = np.concatenate(u_final, axis = 0)
		if total_relerr < tol:
			breakflag = True
	
	breakflag = comm.bcast(breakflag,root=0)
endtime = MPI.Wtime()	
if rank == 0:
    print("\nTime elapsed:{} s".format(endtime - starttime))
    print("\nNo. of processes used = {}".format(nproc))
    print("\nRelative L1 error = {}".format(total_relerr))
    u_final_flip = np.flip(u_final)
    u_final = np.concatenate([u_final,u_final_flip[1:]])
    y = np.arange(0,L+dely,dely)
    plt.plot(u_final,y)
    plt.xlabel("x-velocity, u_x")
    plt.ylabel("y")
    plt.title("Poisuelle Flow")
    plt.show()
