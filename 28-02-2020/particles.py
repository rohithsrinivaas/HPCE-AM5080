#Using periodic boundary condition

from mpi4py import MPI
import numpy as np
import time
import matplotlib.pyplot as plt

comm = MPI.COMM_WORLD
nproc = comm.Get_size()
rank = comm.Get_rank()
P = 100
dom_size = 1
N = 1000
np.random.seed(int(time.time()))
class particle:
	pid = None
	loc = 0.0
	def __init__(self,pid,loc):
		self.pid = pid
		self.loc = loc	

plist = []
for i in range(rank*P/nproc,(rank+1)*P/nproc):
	loc = np.random.random()
	plist.append(particle(i,loc))
for obj in plist:
	print(obj.pid,obj.loc)

target_id = 42
target_path = []
for m in range(0,N):
	out_right = []
	out_left = []
	for p in plist:	
		step = np.random.random()-0.5
		current_loc = p.loc
		if p.pid == target_id:
			target_path.append((m,dom_size*rank+p.loc))
		new_loc = current_loc + step
		if new_loc > dom_size:
			p.loc = new_loc - dom_size
			out_right.append(p)
		if new_loc < 0:
			p.loc = new_loc + dom_size
			out_left.append(p)
	
	for obj in out_right:
		plist.remove(obj)
	for obj in out_left:
		plist.remove(obj)

	comm.send(out_left, dest = (rank-1)%nproc, tag = 1)
	comm.send(out_right, dest = (rank+1)%nproc, tag = 2)
	in_right = comm.recv(source = (rank+1)%nproc, tag = 1)
	in_left = comm.recv(source = (rank-1)%nproc, tag = 2)
	comm.barrier()
	for obj in in_right:
		plist.append(obj)
	for obj in in_left:
		plist.append(obj)
data = comm.gather(target_path, root = 0)
if rank == 0:
	flat_data = []
	for sublist in data:
		for item in sublist:
			flat_data.append(item)
	flat_data_sorted = sorted(flat_data, key = lambda x: x[0])
	x,y = zip(*flat_data_sorted)
	plt.plot(x,y)
	plt.title("Particle #{}".format(target_id))
	plt.xlabel('Time')
	plt.ylabel('Position')
	plt.show()

	
	
	
