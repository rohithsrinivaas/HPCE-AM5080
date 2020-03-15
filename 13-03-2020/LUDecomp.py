# Program to decompose a matrix to LU form
# Importing the required libraries 
import math
import random 
import numpy as np	
from mpi4py import MPI
import seaborn as sns
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nProcs = comm.Get_size()
size = nProcs
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
random.seed(1)
m = None 
k = None 
n = None 
A = None 
if rank == 0:
	A = np.array([[1.00,0.00,1,2],[0,1,-2,0],[1,2,-1,0],[2,1,3,-2.00]])
	m,n = np.shape(A)
	print A
	for i in range(m):
		col_max = A[i,i]
		ind_max = i
		for j in range(i+1,n):
			if A[j,i]>=col_max:
				col_max = A[j,i]
				ind_max = j
		A[[i,ind_max]]=A[[ind_max,i]]
	print A
m = comm.bcast(m,root = 0)
n = comm.bcast(n,root = 0)
B = np.full(n,1.00)
sub_row = np.full(n,1.00)
comm.Scatter(A,B,root = 0)
# print B
iter = 0
while iter < m:
	if rank == iter:
		sub_row = B
	sub_row = comm.bcast(sub_row,root=iter)
	comm.barrier()
	if rank > iter:
	 	alpha = (B[iter]/sub_row[iter])
	 	for i in range(n):
	 		B[i] = B[i] - alpha*sub_row[i]
	iter+=1
	comm.barrier()
comm.Gather(B,A,root=0)
if rank ==0:
	print A


# 	A = np.random.rand(4,6)
# 	B = np.random.rand(6,6)
# 	print  A
# 	print B
# 	m,k = np.shape(A)
# 	k,n = np.shape(B)
# 	C = np.full((m,n),0.00)
# # To factorize nProc so that iProcs/jProcs ~ iLength/jLength
# k = comm.bcast(k,root = 0)
# if nProcs == 4:
# 	iProcs = 2 
# 	jProcs = 2
# elif nProcs == 6:
# 	if m>n:
# 		jProcs = 3
# 		iProcs = 2
# 	else: 
# 		iProcs = 2
# 		jProcs = 3
# iLength = m/iProcs
# jLength = n/jProcs
# # print("iProcs = {}, jProcs = {}").format(iProcs,jProcs)
# if rank == 0:
# 	k = 0
# 	for i in range(0,iProcs):
# 		for j in range(0,jProcs):
# 			rows = A[i*iLength:(i+1)*iLength,:]
# 			rows.tolist() 
# 			cols = B[:,j*jLength:(j+1)*jLength]
# 			comm.send(rows, dest = i*jProcs+j, tag = 0)
# 			comm.send(cols, dest = i*jProcs+j, tag = 0) 
# rows = None 
# cols = None 
# rows = comm.recv(source = 0,tag = 0)
# cols = comm.recv(source = 0,tag = 0)
# # print("Rows - {}, cols - {} for Rank - {}").format(rows,cols,rank)
# ans = np.dot(rows,cols)
# # print ans
# comm.send(ans, dest = 0, tag = 0)
# if rank == 0:
# 	final_ans = None
# 	for i in range(iProcs):
# 		row_ans = None
# 		for j in range(jProcs):
# 			segment = comm.recv(source = i*jProcs+j, tag = 0)
# 			segment = np.asarray(segment)
# 			# print segment
# 			if j == 0:
# 				row_ans = segment
# 			else:
# 				row_ans = np.hstack((row_ans,segment))
# 			# print("RowAns - {} ").format(row_ans)
# 		if i ==0:
# 			final_ans = row_ans
# 		else:
# 			final_ans = np.vstack((final_ans,row_ans))
# 	print final_ans
# 	print np.dot(A,B)


# print("Rank - {}, Data - {}").format(rank,data)
# shift_x = rank%jProcs
# shift_y = rank/jProcs
# if rank <iProcs:
# 	for j in range(jProcs):
# 		comm.send(data,dest = shift_x*jProcs+j,tag = shift_x)
# else:
# 	for i in range(iProcs):
# 		comm.send(data,dest = i*jProcs+shift_y,tag = shift_y)
# comm.recv()
# # iProc = 







# Declaring the array and setting the seed for random
# del_x = 0.025
# del_y = 0.025
# del_x = 0.0025
# del_y = 0.0025
# del_t = 0.1 
# length = 0.2
# time_max = 1000
# alpha = 10**(-4)
# r = alpha * del_t /(del_x**2)
# size_list = int(length/(del_x*(nProcs)**0.5))
# side_size = int(length/(del_x))
# block_size = size_list*size_list
# local_temp = np.full((size_list,size_list),0.00)
# temp_1 = local_temp
# temp_2 = local_temp
# if rank == 0:
# 	local_temp[:,0]= 300.00
# 	local_temp[0,:] = 400.00
# elif rank == 1:
# 	local_temp[:,size_list-1] = 100
# 	local_temp[0,:] = 400.00
# elif rank == 2:
# 	local_temp[:,0] = 300.00
# else :
# 	local_temp[:,size_list-1] = 100.00
# global_temp = None
# local_temp = np.reshape(local_temp,(1,block_size))
# # print(local_temp)
# local_temp.tolist()
# comm.send(local_temp, dest=0, tag=rank**2)
# open('Temperature_Profile.txt', 'w').close()	
# # print(local_temp)
# comm.barrier()
# if rank == 0:
# 	# print "Printing the Received buffer"
# 	local_temp_0 = None 
# 	local_temp_1 = None
# 	local_temp_2 = None
# 	local_temp_3 = None
# 	local_temp_0 = comm.recv(source=0, tag=0)
# 	local_temp_1 = comm.recv(source=1, tag=1)
# 	local_temp_2 = comm.recv(source=2, tag=4)
# 	local_temp_3 = comm.recv(source=3, tag=9)
# 	local_temp_0 = np.asarray(local_temp_0)
# 	local_temp_1 = np.asarray(local_temp_1)
# 	local_temp_2 = np.asarray(local_temp_2)
# 	local_temp_3 = np.asarray(local_temp_3)
# 	local_temp_0 = np.reshape(local_temp_0,(size_list,size_list))
# 	local_temp_1 = np.reshape(local_temp_1,(size_list,size_list))
# 	local_temp_2 = np.reshape(local_temp_2,(size_list,size_list))
# 	local_temp_3 = np.reshape(local_temp_3,(size_list,size_list))
# 	# print(local_temp_0)
# 	# print(local_temp_1)
# 	# print(local_temp_2)
# 	# print(local_temp_3)
# 	global_hor_1 = np.hstack((local_temp_0,local_temp_1))
# 	global_hor_2 = np.hstack((local_temp_2,local_temp_3))
# 	global_temp = np.vstack((global_hor_1,global_hor_2))
# 	# print global_temp
# 	global_temp.tolist()
# global_temp = comm.bcast(global_temp,root=0)
# global_temp = np.asarray(global_temp)
# global_temp = np.reshape(global_temp,(size_list*2,size_list*2))
# if rank ==0:
# 	print global_temp
# comm.barrier()
# origin_shift_x = 0
# origin_shift_y = 0
# if rank == 1:
# 	origin_shift_y = size_list
# elif rank == 2:
# 	origin_shift_x = size_list
# elif rank == 3:
# 	origin_shift_x = size_list
# 	origin_shift_y = size_list
# else:
# 	origin_shift_y = 0
# 	origin_shift_x = 0
# local_temp = np.reshape(local_temp,(size_list,size_list))
# # print("Printing local Temp - {}").format(local_temp)
# # print np.shape(global_temp)
# time_iter = 1
# while time_iter <= 1:
# 	diff_temp = np.full((size_list,size_list),0.00)
# 	for i in range(size_list):
# 		for j in range(size_list):
# 			x = origin_shift_x + i
# 			y = origin_shift_y + j
# 			if x == 0 or y == 0 or y == side_size-1:
# 				diff_temp[i,j] = 0
# 			elif x == side_size-1:
# 				diff_temp[i,j] = r*(global_temp[x,y+1] + global_temp[x,y-1] + 2*global_temp[x-1,y] - 4 * global_temp[x,y])/4 
# 			elif x>=0 and y>=0 and x<side_size and y<side_size:
# 				diff_temp[i,j] = r*(global_temp[x+1,y] + global_temp[x,y+1] + global_temp[x,y-1] + global_temp[x-1,y] - 4 * global_temp[x,y])/4
# 			else:
# 				print("Index out of bounds - x - {} y - {} i - {} j - {} rank - {}").format(x,y,i,j,rank) 
# 	local_temp = np.add(local_temp,diff_temp)
# 	# print("Rank = {}, local temp - {}").format(rank,local_temp)
# 	local_temp.tolist()
# 	comm.send(local_temp, dest=0, tag=rank**2)
# 	# print(local_temp)
# 	comm.barrier()
# 	if rank == 0:
# 		# print "Printing the Received buffer"
# 		local_temp_0 = None 
# 		local_temp_1 = None
# 		local_temp_2 = None
# 		local_temp_3 = None
# 		local_temp_0 = comm.recv(source=0, tag=0)
# 		local_temp_1 = comm.recv(source=1, tag=1)
# 		local_temp_2 = comm.recv(source=2, tag=4)
# 		local_temp_3 = comm.recv(source=3, tag=9)
# 		local_temp_0 = np.asarray(local_temp_0)
# 		local_temp_1 = np.asarray(local_temp_1)
# 		local_temp_2 = np.asarray(local_temp_2)
# 		local_temp_3 = np.asarray(local_temp_3)
# 		local_temp_0 = np.reshape(local_temp_0,(size_list,size_list))
# 		local_temp_1 = np.reshape(local_temp_1,(size_list,size_list))
# 		local_temp_2 = np.reshape(local_temp_2,(size_list,size_list))
# 		local_temp_3 = np.reshape(local_temp_3,(size_list,size_list))
# 		# print(local_temp_0)
# 		# print(local_temp_1)
# 		# print(local_temp_2)
# 		# print(local_temp_3)
# 		global_hor_1 = np.hstack((local_temp_0,local_temp_1))
# 		global_hor_2 = np.hstack((local_temp_2,local_temp_3))
# 		global_temp = np.vstack((global_hor_1,global_hor_2))
# 		# print global_temp
# 		global_temp.tolist()
# 	global_temp = comm.bcast(global_temp,root=0)
# 	global_temp = np.asarray(global_temp)
# 	global_temp = np.reshape(global_temp,(size_list*2,size_list*2))
# 	local_temp = np.asarray(local_temp)
# 	local_temp = np.reshape(local_temp,(size_list,size_list))
# 	time_iter += 1
# if rank ==0:
# 	print global_temp
# 	plot_temp = sns.heatmap(global_temp)
# 	fig = plot_temp.get_figure()
# 	fig.savefig("time_iter.png")
# 	fig.clf()
# 	temp_csv = np.reshape(global_temp,(1,side_size**2))
# 	with open("Temperature_Profile.txt", "a") as myfile:
# 	 	np.savetxt(myfile, temp_csv, fmt='%1.4e', delimiter=",")