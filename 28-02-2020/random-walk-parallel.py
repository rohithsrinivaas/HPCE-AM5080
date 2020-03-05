from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt


comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()

P = 10;
num_particles = int(np.ceil(P/nprocs))
x_width = float(P)/nprocs


num_iters = 10;
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
	loc = np.random.uniform(rank*x_width,(rank+1)*x_width)
	plist.append(particle(i+rank*(num_particles),loc))

leaving_right  = [];
leaving_left = [];
incoming_right = [];
incoming_left = [];

target_particle = np.random.randint(num_particles)
 
for t in range(num_iters):
	if rank < nprocs:
		for i in range(len(plist)):
			plist[i].move(np.random.uniform(-step_length,step_length))
			if plist[i].show_loc() >= rank*x_width and plist[i].show_loc() < (rank+1)*x_width :
				continue;
			elif plist[i].show_loc() >= (rank + 1)*x_width:
				leaving_right.append(plist[i]);	 
			elif plist[i].show_loc() < rank*x_width:
				leaving_left.append(plist[i]);

	plist = list(set(plist) - set(leaving_right) - set(leaving_left))	
	


	if rank == 0:
		for j in range(len(leaving_left)):
			print(leaving_left[j].show_loc(),rank)
			print("LALALAL")
			leaving_left[j].move(float(P))
			print(leaving_left[j].show_loc(),rank)
		comm.send(leaving_right,dest = 1);
		comm.send(leaving_left,dest = nprocs-1);
		incoming_right = comm.recv(source = 1)
		incoming_left = comm.recv(source = nprocs - 1);
		plist = plist + incoming_right + incoming_left

	elif rank == nprocs - 1 :
		for j in range(len(leaving_right)):
			print(leaving_right[j].show_loc(),rank)
			print("LALALAL")
			leaving_right[j].move(-float(P))
			print(leaving_right[j].show_loc(),rank)	
		comm.send(leaving_right,dest = 0);
		comm.send(leaving_left,dest = nprocs-2);
		incoming_right = comm.recv(source = 0)
		incoming_left = comm.recv(source = nprocs - 2);
		plist = plist + incoming_right + incoming_left
	elif rank < (nprocs -1) and rank > 0 :
		comm.send(leaving_right,dest = rank+1);
		comm.send(leaving_left,dest = rank -1);
		incoming_right = comm.recv(source = rank+1);
		incoming_left = comm.recv(source = rank-1);
		plist = plist + incoming_right + incoming_left
	comm.barrier();
	
	

	#tracking the position of given particle id
	'''
	for i in range(len(plist)):
		if plist[i].show_pld() == target_particle:
			print(str(plist[i].show_loc())+','+str(rank))
	'''

	
	
