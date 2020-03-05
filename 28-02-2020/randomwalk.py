from mpi4py import MPI
from random import randint
import numpy as np
import matplotlib.pyplot as plt
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
Particles=100
p=int(Particles/size)
niter=5000

class particle:
	pid=None
	loc=0
	def __init__(self,pid,loc):
		self.pid=pid
		self.loc=loc

# Normal Particle distribution
plist=[]
plen=[p]
target_id=4 
motion=[]
l,u=int(rank*p),int((rank+1)*p)
for i in range(l,u):
	plist.append(particle(i,i))
u=u-1

for i in range(niter): # Number of iterations for random walk
	for j in range(len(plist)):
		curr =plist[j] # Current particle
		move=randint(0,1)
		if move==0:
			move=-1		
		curr.loc=curr.loc+move
	comm.barrier()	

	forward=[x for x in plist if x.loc>u]
	backward=[y for y in plist if y.loc<l]

	comm.send(forward,dest=(rank+1)%4)
	comm.send(backward,dest=(size+rank-1)%4)
	
	comm.barrier()
	
	frec=comm.recv(source=(rank-1)%4)
	brec=comm.recv(source=(rank+1)%4)
	
	for k in frec:
		if k.loc==Particles:
			k.loc=0
		plist.append(k)
	comm.barrier()	

	for k in brec:
		if k.loc==-1:
			k.loc=Particles-1
		plist.append(k)

	comm.barrier()	
	plist=[x for x in plist if x.loc<=u and x.loc>=l] 
	plen.append(len(plist))
	if i==niter-1:
		print('Initial and final number of particle in rank',rank,'are:',p, len(plist))

if rank==1:
	print('The sum of particle is equal to total number of particles: ',Particles)
	plt.plot(list(range(niter+1)),plen)
	plt.show()
	plt.plot()	
