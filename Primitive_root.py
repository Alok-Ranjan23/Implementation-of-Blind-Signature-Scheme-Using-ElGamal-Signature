import modu

# nth prime number
def is_prime(count, primes):
	for prime in primes:
		if not (count == prime or count % prime):
			return False
	primes.add(count)
	return count

def nth_prime(n):
	primes = set([2])
	count= 2
	count_prime = 0
	while True:
		if is_prime(count, primes):
			count_prime += 1
			if count_prime == n:
				return primes
		count += 1

def prime_factor(num):
	x = set([])
	for i in range(2,num//2+1):
		while(num%i==0):
			x.add(i)
			num = num/i
		if(num==1):
			break
	return(x)


def primitive_root(n):
	phi = n-1
	factor_list = sorted(list(prime_factor(phi)))
	for i in range(2,phi+1):
		flag = 0
		for j in factor_list:
			if(modu.modular_exp(i,phi//j,n)==1):
				flag = 1
				break;
		if(flag==0):
			return(i)
	return(-1)
    	

#n = int(input("Enter n to computer nth prime"))

#p = sorted(list(nth_prime(n)))[-1]

#print(p," : - Form group over",p)

#Primitive root of p

#g = primitive_root(p)
#print("Smallest Primitive Root of ", p , " is ", g)

