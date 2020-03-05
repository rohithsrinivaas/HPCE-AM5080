import numpy as np


def bubblesorting(a):
	n = len(a)
	for i in range(n-1):
		print(a)
		for j in range(0,n-i-1):
			if( a[j] >= a[j+1] ):
				temp = a[j+1]
				a[j+1] = a[j]
				a[j] = temp;
	return a;




arr =  np.random.randint(low = 0, high =  40, size = 10)
print("Random array is : ")
print(arr)
print("Sorted Array is : (Ascending)")	
print(bubblesorting(arr))
