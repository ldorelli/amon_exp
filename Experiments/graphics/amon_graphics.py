import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def degree_histogram(data, b):

	plt.subplot(2, 1, 1)
	# values, base = plt.hist(data, bins=b)	
	plt.title('Degree Distribution')
	plt.xlabel('Degree')
	plt.ylabel('Frequency')
	
	plt.subplot(2, 1, 2)


	cumulative = np.cumsum(values)
	plt.plot(cumulative)
