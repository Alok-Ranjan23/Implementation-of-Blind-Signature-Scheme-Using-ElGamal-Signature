import socket
import Primitive_root



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



def max_element(lst):
	max_el = lst[0]
	for i in range(1,len(lst)):
		if max_el < lst[i]:
			max_el = lst[i]
	return(max_el)



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



def bank(mod_msg,xa,r,k):
	
	##Inverse of k_a
	ki = modular_mul_inv(k,p-1)
	
	##mod_msg list
	mod_msg_list = list()
	for i in mod_msg:
		j = ord(i)
		mod_msg_list.append(j)
		
	#print("Message list for signing: ",mod_msg_list)
	
	#Singed_list Generation
	sign_list = list()
	
	for i in mod_msg_list:
		y1 = i%(p-1)
		y2 = (xa*r)%(p-1)
		C = (((y1 - y2)%(p-1)) * ki)%(p-1)
		sign_list.append(C)
	
	#print("Signed List for Message: ",sign_list)
	
	
	##Signed_Message:
	sign_msg = ''
	
	for i in sign_list:
		j = chr(i)
		sign_msg = sign_msg + j
	
	return(sign_msg)



s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("Socket Created Successfully")

port = 12346

s.bind(('127.0.0.1',port))

print("Socket blinded to %s"%(port))

s.listen()

print("Socket is listening")

c,addr = s.accept()
print("Got Connection from",addr)

rev = int(c.recv(1024))

'''
rev_c = ''
for i in rev:
	if(i != 'b' and i != '\''):
		rev_c = rev_c + i
'''

p = max(Primitive_root.nth_prime(rev))
print(type(p))
a = Primitive_root.primitive_root(p)
print("Primitive root of : ",rev,"th prime ",p," is ",a)


c_n = bytes(str(a),"ascii")
c.send(c_n)

print()
print("A large prime and its primitive root is a global information")
print()



##Secret Key of Alice
x_a = int(c.recv(1024))
print("Private key of Alice: ",x_a)
c.sendall(b'Private key is send.')



##ElGamal Secret of Alice
k_a = int(c.recv(1024))
print("ElGamal Secret of Alice: ",k_a)
c.sendall(b'ElGamal Secret is send.')



##r Secret of Alice
r_a = int(c.recv(1024))
print("r Secret of Alice: ",r_a)
c.sendall(b'r Secret is send.')

##Message to be signed
#msg = ((s.recv(1024).decode()))
m_a = ((c.recv(1024).decode()))
print(" Message send for signing by Alice: ",m_a)
c.sendall(b' Message for signing is send.')



blind_s = bank(m_a,x_a,r_a,k_a)
print()
print()
print("Signed Message for Alice: ",blind_s)
print()
#c.send(str(mod_blind).encode())
c_blind_s =str(blind_s).encode()

c.sendall(c_blind_s)

s_msg3 = str(c.recv(1024))

c_msg3 = ''
for i in s_msg3:
	if(i != 'b' and i != '\''):
		c_msg3 = c_msg3 + i
		
print(c_msg3)



c.close()
	
	
	
	