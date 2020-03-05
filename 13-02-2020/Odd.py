# Program to sort a given array using 4 processes  
# Importing the required libraries 
import math
import random 
import numpy as np	
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
n = size
# Declaring the array and setting the seed for random
size_list = 8
random_list = []
random.seed(4)
# Initializing the random array 
if rank ==0:
	for i in range(size_list):
		random_number = random.randint(1,40)
		random_list.append(random_number)
	print(random_list)
sorted = 0
iter = 1
sorted = 1
# Spliting the array to processes with two each for a process 
if rank ==0:
	for i in range(size_list):
		comm.send(random_list[i],dest = int(i/2),tag=0)
data_1 = comm.recv(source = 0, tag =0)
data_2 = comm.recv(source = 0, tag =0)
# Flag variable to check whether the array is sorted or not 
sorted = 0
# Loop to recursively sort the array 
while iter < 100 and sorted == 0:
#	print("Before Sorting - Iter - {} Rank {} - Elements - {} {}").format(iter,rank,data_1,data_2)	
	sorted = 1
# Based on the iter value the ODD or EVEN position swapping will take place
	if iter%2 == 0:	# If its even, then the adjacent elements in a process will be swapped
		if data_1 > data_2:
			temp = data_2
			data_2 = data_1
			data_1 = temp
	else:		# If its odd, adjacent element of different process will be swapped
		# For Rank = 0 and N-1, we have edge cases to be included
		# For other ranks, send the left element to rank-1 and right element to rank+1 		
		if rank == 0:	
			comm.send(data_2, dest = 1, tag = iter)
		elif rank == n-1:
			comm.send(data_1,dest = n-2, tag = iter)
		else:			 
			comm.send(data_1,dest=rank-1, tag = iter)
			comm.send(data_2,dest=rank+1, tag = iter)
		# Receive the elements and swap if needed
		if rank == 0:
			data_r = comm.recv(source = 1, tag = iter)
			if data_2 > data_r:			
				temp = data_2
				data_2 = data_r
				data_r = temp
		elif rank == n-1:
			data_l = comm.recv(source = n-2, tag = iter)
			if data_l > data_1: 
				temp = data_1
				data_1 = data_l
				data_l = temp
		else:			 
			data_l = comm.recv(source = rank-1, tag = iter)
			data_r = comm.recv(source = rank+1, tag = iter)
			if data_l > data_1: 
				temp = data_1
				data_1 = data_l
				data_l = temp
			if data_2 > data_r:			
				temp = data_2
				data_2 = data_r
				data_r = temp
	iter += 1
	print("Rank {} - Elements - {} {}").format(rank,data_1,data_2)
	# Sending all the array elements and gathering in Rank - 0 to check whether the array is sorted or not 
	comm.send(data_1, dest = 0, tag = 0)
	comm.send(data_2, dest = 0, tag = 1)
	if rank ==0:
		# Array is gathered using the rank and tag sequentially 
		for i in range(0,size_list,2):
			left = comm.recv(source = int(i/2),tag=0)
			right = comm.recv(source = int(i/2),tag=1)
			random_list[i] = left
			random_list[i+1] = right
		# Partially sorted array is printed on the screen
		print random_list
		# Checking whether the array is sorted or not 
		for i in range(len(random_list)-1):
			if random_list[i] > random_list[i+1]:
				sorted = 0
	# Broadcasting the result whether the array is sorted or not 
	sorted = comm.bcast(sorted,root=0)
# Gathering the elements to consolidate the final array 
comm.send(data_1, dest = 0, tag = 0)
comm.send(data_2, dest = 0, tag = 1)
if rank ==0:
	for i in range(0,size_list,2):
		data_1 = comm.recv(source = int(i/2),tag=0)
		data_2 = comm.recv(source = int(i/2),tag=1)
		random_list[i] = data_1
		random_list[i+1] = data_2
	print "The Sorted Array is as follows:"
	print random_list

