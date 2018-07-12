import socket
import modu
import random
import sys

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



def max_element(lst):
	max_el = lst[0]
	for i in range(1,len(lst)):
		if max_el < lst[i]:
			max_el = lst[i]
	return(max_el)


def gcd(num1,num2):
	if(num2 == 0):
		return(num1)
	
	elif(num1 == 0):
		return(num2)
	
	elif(num1%num2==0):
		return(num2)
	
	else:
		rem = num1%num2
		return(gcd(num2,rem))


def extended_gcd(num1,num2):
	##Base Case
	if(num2==0):
		return(num1,1,0)
	##Recursive Step
	else:
		d,a,b = extended_gcd(num2,num1%num2)
		return(d,b,a-(num1//num2)*b)



def modular_mul_inv(num,n) :
	hcf,x,y = extended_gcd(num,n)
	
	if hcf==1:
		return((x%n+n)%n)



def RSA_key():
	n1 = input("Enter n to generate nth prime as one of the factor(p)")
	n1 = int(n1)
	n2 = input("Enter n to generate nth prime as one of the factor(q)")
	n2 = int(n2)
	p = max_element(list(nth_prime(n1)))
	q = max_element(list(nth_prime(n2)))
	
	print("p : ",p)
	print("q : ",q)
	
	n = p*q
	
	print("n : ",n)
	
	phi_n = (p-1)*(q-1)
	
	## Find e
	e = 0
	for i in range(2,n-1):
		if gcd(i,phi_n) == 1 :
			e = i
			break
	
	print("public_key : ", e,n)
	
	## Find d : e.d = 1(mod phi_n) i.e. d is multiplicative inverse of e modulo phi_n 
	d = modular_mul_inv(e,phi_n)
	
	print("private_key : ",d,n)
	
	return(e,d,n)
	


def init_RSA_key():
	global e,n,d
	e,d,n = RSA_key()
	return(e,d,n)



def sign_msg(message):
	
	msg_list = list()
	for i in message:
		j = ord(i)
		msg_list.append(j)
		
	sign_list = list()
	for i in msg_list:
		k = modu.modular_exp(i,d,n)
		sign_list.append(k)
	print()
	#print("Sign_list: ",sign_list)
	print()
	sign_msg = ''
	for i in sign_list:
		j = chr(i)
		sign_msg = sign_msg + j
	
	return(sign_msg)



s = socket.socket()

port = 12347

s.connect(('127.0.0.1',port))

e,d,n = init_RSA_key()

print(e)
print(n)
#sn_1 = bytes(str(e),"ascii")
#print(sn_1)
#sn_2 = bytes(str(n),"ascii")
#print(sn_2)
s.sendall(bytes(str(e),"ascii"))

print(s.recv(1024))
print()
s.sendall(bytes(str(n),"ascii"))

msg = ((s.recv(1024).decode()))

print("Msg To signed: ",msg)
print()

signed_msg = sign_msg(msg)

print("Signed_Msg: ",signed_msg)
print()

s.send(signed_msg.encode())

s.close()
