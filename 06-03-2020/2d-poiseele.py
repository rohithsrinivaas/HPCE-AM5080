from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt


comm = MPI.COMM_WORLD
p = comm.Get_size()
r = comm.Get_rank()

xi = 0
xf = 0.2
dx = 0.025
nx = int(((xf - xi) / dx) + 1)

yi = 0
yf = 0.2
dy = 0.025
ny = int(((xf - xi) / dx) + 1)

ti = 0
tf = 50
dt = 0.1
alpha=  1
cfl = alpha*dt/(dx^2) #should be less than or equal to .5 for convergence
nt = int(((tf - ti) / dt) + 1)


tx = int(np.ceil(1.0*nx/2))
ty = int(np.ceil(1.0*ny/2))


numy = (min(ny,tx*(r+1))) - (tx*r+1) + 1
numx = (min(nx,ty*(r+1))) - (ty*r+1) + 1


# block domain decomposition

'''
rank 0 : [0:nx/2][0:ny/2]
rank 1 : [nx/2:nx][0:ny/2]
rank 2 : [0:nx/2][ny/2:ny]
rank 3 : [nx/2:nx][ny/2:ny]
'''
if r==0:
	# u = np.zeros([nt,nx])
	curr = np.zeros((numx+1,numy+1))
	curr[:] = 300
	next = curr
elif r==p-1:
	curr = np.zeros((numx+1,numy+1))
	curr[:] = 300
	curr[-1] = 500
	next = curr
else:
	curr = np.zeros((numx+2,numy+2))
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
