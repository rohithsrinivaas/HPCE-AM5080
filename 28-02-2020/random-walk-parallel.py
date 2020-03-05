from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt


comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()

P = 10;
num_particles = int(np.ceil(P/nprocs))
x_width = P/nprocs


num_iters = 1;
step_length = (x_width/4);


class particle:
	pld =  None;
	loc = 0.0;
	def __init__(self, pld, loc):
		self.pld = pld		
		self.loc = loc
		
	def show_pld(self):
		return self.pld
	def show_loc(self):
		return self.loc
	def move(self,x):
		self.loc = self.loc + x;
plist = []
for i in range(num_particles):
	percent = np.random.random()
	loc = x_width*(rank*(1 - percent) + (rank+1)*percent)
	plist.append(particle(i+rank*(num_particles),loc))	
	

for t in range(num_iters):
	for i in range(num_particles):
		plist[i].move(np.random.uniform(-step_length,step_length,1)[0])
		print(plist[i].show_pld(),plist[i].show_loc(),rank)


		if plist[i].show_loc() > (rank+1)*x_width and plist[i].show_loc() <= (rank+2)*x_width and rank != nprocs - 1:
			comm.send(plist[i],dest = rank + 1)
			addon = comm.recv(source = rank - 1)		
		if plist[i].show_loc() < 0:
				#send to nprocs-1
		elif rank == nprocs - 1:
			
	
		else:
	
