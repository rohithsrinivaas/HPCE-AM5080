from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt


comm = MPI.COMM_WORLD
p = comm.Get_size()
r = comm.Get_rank()

xi = 0
xf = 1
dx = 0.01
nx = int(((xf - xi) / dx) + 1)
ti = 0
tf = 1000
dt = 0.1
cfl = 0.45 #should be less than or equal to .5 for convergence
nt = int(((tf - ti) / dt) + 1)
t = int(np.ceil(1.0*nx/p))



num = (min(nx,t*(r+1))) - (t*r+1) + 1
if r==0:
	# u = np.zeros([nt,nx])
	curr = np.zeros(num+1)
	curr[:] = 300
	next = curr
elif r==p-1:
	curr = np.zeros(num+1)
	curr[:] = 300
	curr[-1] = 500
	next = curr
else:
	curr = np.zeros(num+2)
	curr[:] = 300
	next = curr
comm.barrier()



for i in range(1,nt):
	next[1:-1] = curr[1:-1] + cfl*(curr[0:-2] - (2*curr[1:-1]) + curr[2:])
	if r>0 and r<(p-1):
		comm.send(next[1],dest=r-1)
		comm.send(next[-2],dest=r+1)
		next[0] = comm.recv(source=r-1)
		next[-1] = comm.recv(source=r+1)
	elif r==0:
		next[-1] = comm.recv(source=r+1)
		comm.send(next[-2],dest=r+1)
	else:
		next[0] = comm.recv(source=r-1)
		comm.send(next[1],dest=r-1)
	comm.barrier()
	curr = next
if r==0:
	T = curr[0:-1]
elif r==p-1:
	T = curr[1:]
else:
	T = curr[1:-1]
T_final = np.array(comm.gather(T, root=0))

if r==0:
	T_final_plot = T_final[0]
	for i in range(1,p):
		T_final_plot = np.append(T_final_plot,T_final[i])
	x = np.arange(xi,xf+dx,dx)
	plt.plot(x,T_final_plot)
	plt.show()
