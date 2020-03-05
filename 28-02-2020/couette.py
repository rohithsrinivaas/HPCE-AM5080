from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
comm = MPI.COMM_WORLD
p = comm.Get_size()
r = comm.Get_rank()
# def fn(x):
# 	return x**2;
yi = 0
yf = 10
dy = 0.1
ny = int(((yf - yi) / dy) + 1)
ti = 0
tf = 500000
dt = 50
mu = 0.089
rho = 1000
cfl = mu * dt / (rho * dy * dy) #should be less than or equal to .5 for convergence
nt = int(((tf - ti) / dt) + 1)
t = int(np.ceil(1.0*ny/p))

nyr = (min(ny,t*(r+1))) - (t*r+1) + 1
if r==0:
	# u = np.zeros([nt,ny])
	u0 = np.zeros(nyr+1)
	# u0[:] = 300
	u1 = u0
elif r==p-1:
	u0 = np.zeros(nyr+1)
	# u0[:] = 300
	u0[-1] = 5
	u1 = u0
else:
	u0 = np.zeros(nyr+2)
	# u0[:] = 300
	u1 = u0
comm.barrier()

if r==0:
	u = u0[0:-1]
elif r==p-1:
	u = u0[1:]
else:
	u = u0[1:-1]
ui = np.array(comm.gather(u, root=0))
if r==0:
	uip = ui[0]
	for i in range(1,p):
		uip = np.append(uip,ui[i])
comm.barrier()

for i in range(1,nt):
	# if r>0 and r<(p-1):
	u1[1:-1] = u0[1:-1] + cfl*(u0[0:-2] - (2*u0[1:-1]) + u0[2:])
	if r>0 and r<(p-1):
		comm.send(u1[1],dest=r-1)
		comm.send(u1[-2],dest=r+1)
		u1[0] = comm.recv(source=r-1)
		u1[-1] = comm.recv(source=r+1)
	elif r==0:
		u1[-1] = comm.recv(source=r+1)
		comm.send(u1[-2],dest=r+1)
	else:
		u1[0] = comm.recv(source=r-1)
		comm.send(u1[1],dest=r-1)
	comm.barrier()
	u0 = u1

	if i == nt/4:
		pass
		if r==0:
			u = u0[0:-1]
		elif r==p-1:
			u = u0[1:]
		else:
			u = u0[1:-1]
		uf1 = np.array(comm.gather(u, root=0))
		if r==0:
			uf1p = uf1[0]
			for i in range(1,p):
				uf1p = np.append(uf1p,uf1[i])
		comm.barrier()

	if i == nt/2:
		pass
		if r==0:
			u = u0[0:-1]
		elif r==p-1:
			u = u0[1:]
		else:
			u = u0[1:-1]
		uf2 = np.array(comm.gather(u, root=0))
		if r==0:
			uf2p = uf2[0]
			for i in range(1,p):
				uf2p = np.append(uf2p,uf2[i])
		comm.barrier()

	if i == 3*nt/4:
		pass
		if r==0:
			u = u0[0:-1]
		elif r==p-1:
			u = u0[1:]
		else:
			u = u0[1:-1]
		uf3 = np.array(comm.gather(u, root=0))
		if r==0:
			uf3p = uf3[0]
			for i in range(1,p):
				uf3p = np.append(uf3p,uf3[i])
		comm.barrier()

if r==0:
	u = u0[0:-1]
elif r==p-1:
	u = u0[1:]
else:
	u = u0[1:-1]
uf = np.array(comm.gather(u, root=0))
if r==0:
	ufp = uf[0]
	for i in range(1,p):
		ufp = np.append(ufp,uf[i])
	# print(ufp)
	print("t = {}; dt = {}; dy = {}; mu = {}; rho = {}".format(tf,dt,dy,mu,rho))
	# if cfl>0.5:
	# 	print("solution may be divergent due to r=alpha*dt/(dy^2) > 0.5 ...(CFL condition)")
	y = np.arange(yi,yf+dy,dy)
	# print(x)
	plt.plot(uip,y,uf1p,y,uf2p,y,uf3p,y,ufp,y)
	plt.xlabel('Ux')
	plt.ylabel('y')
	plt.show()