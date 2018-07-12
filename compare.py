import sys
import matplotlib.pyplot as plt
import numpy as np


try:
	f_david = open('chaum.txt','r')
except:
	print("Enter Correct file")
	sys.exit()
	

try:
	f_proposed = open('proposed.txt','r')
except:
	print("Enter Correct file")
	sys.exit()

chaum = f_david.read()
proposed = f_proposed.read()
#print(type(chaum))
print()
#print(type(proposed))

chaum_list = chaum.split()
proposed_list = proposed.split()

print(chaum_list)
print()
print(proposed_list)

chaum_i_list = list()
for i in chaum_list:
	j = float(i)
	chaum_i_list.append(j)



proposed_i_list = list()
for i in proposed_list:
	j = float(i)
	proposed_i_list.append(j)



print()
print(chaum_i_list)
print()
print(proposed_i_list)


fig,ax = plt.subplots()
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(np.arange(len(chaum_i_list)),chaum_i_list, bar_width,alpha=opacity,color='b',label='Chaum')
 
rects2 = plt.bar(np.arange(len(proposed_i_list)) + bar_width, proposed_i_list  ,bar_width,alpha=opacity,color='g',label='ElGamal')


plt.ylabel('Time')
plt.xlabel('Sample')
plt.xticks(np.arange(len(proposed_i_list)) + (bar_width/2), ('sample1', 'sample2', 'sample3', 'sample4','sample5'))
plt.title('Comparison of signature scheme')
plt.legend()

plt.show()

