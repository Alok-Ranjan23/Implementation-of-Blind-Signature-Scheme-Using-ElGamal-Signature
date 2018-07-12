def modular_exp(M,e,n):
	if(e==0):
		return(1)
	elif(e%2==0):
		return((modular_exp((M*M)%n,e//2,n))%n)
	else:
		return((M*modular_exp((M*M)%n,(e-1)//2,n))%n)
	return(C)

