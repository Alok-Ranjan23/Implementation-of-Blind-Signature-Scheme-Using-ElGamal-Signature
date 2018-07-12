import socket
import Primitive_root
import random
import modu
import sys
import time


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



def keys():
	#private
	xa = random.randint(1,p)
	while(gcd(xa,p) != 1):
		xa = random.randint(1,p)
	print("Private_key_A: ",xa)
	
	#public
	global ya
	ya = modu.modular_exp(a,xa,p)
	print("Public_key_A: ",ya)
	
	return(xa)



def ElGamal_secret():
	
	#ElGamal Secret
	global k
	k = random.randint(1,p-1)
	while(gcd(k,p-1) != 1):
		k = random.randint(1,p-1)
	
	return(k)



def r_secret():
	
	##r_secret
	global r
	r = modu.modular_exp(a,k,p)
	
	return(r)



def mod_blind_message():
	
	#Input Message
	global msg
	ch = input("Enter choice : for file input 1 and user input any other number")
	global choice
	choice = int(ch)
	if(choice == 1):
		fname = input("Enter Filename: ")
		try:
			fhand = open(fname,'r')
		except:
			print("Enter correct filename")
			sys.exit()
		msg = fhand.read()
	
	else :	
		msg = input("Enter a string:")

	
	#Input Message List
	msg_list = list()
	for i in msg:
		j = ord(i)
		msg_list.append(j)
	
	#print("Message_list",msg_list)
	
	##Blinding Factor
	global h
	h = random.randint(1,p-1)
	while(gcd(h,p-1) != 1):
		h = random.randint(1,p-1)
	
	#Modified Message List
	mod_msg_list = list()
	for i in msg_list:
		j = (h*i)%(p-1)
		mod_msg_list.append(j)
	
	print()
	print("Blinding Factor: ",h)
	print()
	#print("Modified Message List: ",mod_msg_list)
	
	#Modified Message
	mod_msg = ''
	for i in mod_msg_list:
		j = chr(i)
		mod_msg = mod_msg + j
	
	return(mod_msg)



def generate_sign(blind_msg,x_a):
	
	#Blind List
	blind_list = []
	for i in blind_msg:
		j = ord(i)
		blind_list.append(j)
		
	#print("Blind Signed List: ",blind_list)
	
	#Inverse of ElGamal Secret 
	ki = modular_mul_inv(k,p-1)
	
	#Inverse of Binding Factor 
	hi = modular_mul_inv(h,p-1)
	
	#Actual Signature List
	sign_list = list()	
	for i in blind_list:
		y1 = (x_a*r)%(p-1)
		y2 = (y1*ki)%(p-1)
		y3 = (y2*(hi-1))%(p-1)
		y4 = (hi*i)%(p-1)
		s = (y3+y4)%(p-1)
		sign_list.append(s)
		
	#print("Actual Signature List: ",sign_list)
	
	
	##Actual Signature String
	sign_msg = ''
	for i in sign_list:
		j = chr(i)
		sign_msg = sign_msg + j
		
	return(sign_msg)



def Verifier(act_sign):
	
	#Message List
	msg_list = list()
	for i in msg:
		j = ord(i)
		msg_list.append(j)
	
	#print("Input Message List: ",msg_list)
	
	#Actual Signature List
	act_sign_list = []
	for i in act_sign:
		j = ord(i)
		act_sign_list.append(j)
	
	##Compute a^m mod p
	expect_m = list()
	for i in msg_list:
		m_ex = modu.modular_exp(a,i,p)
		expect_m.append(m_ex)
		
	print()
	print("Expected_list: ",expect_m)
	print()
	
	##Compute (y^r * r^s) mod p
	extract_m = list()
	y_r = modu.modular_exp(ya,r,p)
	for j in act_sign_list:
		r_s = modu.modular_exp(r,j,p)
		m_get = (y_r*r_s)%p
		extract_m.append(m_get)
		
	print()
	print("Extracted_list: ",extract_m)
	print()
	
	##Compare Above Both List expect_m and extract_m 
	temp = 1
	copy_m = list(expect_m)
	for i in copy_m:
		if(i != extract_m[expect_m.index(i)]):
			temp = 0
			print("ElGamal Blind Signature is not successfully done.")
			break
	
	if(temp == 1):
		print("ElGamal Blind Signature is successfully done. ")



s = socket.socket()
stime = time.time()
port = 12346

s.connect(('127.0.0.1',port))

n = int(input("Enter n to generate nth prime : "))

#Form group over p
global p
p = max_element(list(Primitive_root.nth_prime(n)))

s_n = bytes(str(n),"ascii")

s.sendall(s_n)

#Receive Primitive Root
global a
a = int(s.recv(1024))

'''
get_s = ''
for i in rev:
	if(i != 'b' and i != '\''):
		get_s = get_s + i
'''

print("Primitive root of ",p , " is ", a )

print()
print("A large prime and its primitive root is a global information")
print()



#Private Key of Alice
x_alice = keys()

print("Private key of Alice: ",x_alice)

s_x_alice = bytes(str(x_alice),"ascii")

s.sendall(s_x_alice)

c_msg = str(s.recv(1024))

s_msg = ''
for i in c_msg:
	if(i != 'b' and i != '\''):
		s_msg = s_msg + i
		
print(s_msg)



#ElGamal Secret
k_alice = ElGamal_secret()

print("ElGamal Secret of Alice: ",k_alice)
print()

s_k_alice = bytes(str(k_alice),"ascii")

s.sendall(s_k_alice)

c_msg1 = str(s.recv(1024))

s_msg1 = ''
for i in c_msg1:
	if(i != 'b' and i != '\''):
		s_msg1 = s_msg1 + i
		
print(s_msg1)
print()


#r Secret
r_alice = r_secret()

print("r Secret of Alice: ",r_alice)
print()

s_r_alice = bytes(str(r_alice),"ascii")

s.sendall(s_r_alice)

c_msg2 = str(s.recv(1024))

s_msg2 = ''
for i in c_msg2:
	if(i != 'b' and i != '\''):
		s_msg2 = s_msg2 + i
		
print(s_msg2)


##Modified Message to send for signing
mod_msg_alice = mod_blind_message()

print("Modified Message of Alice: ",mod_msg_alice)
print()

#c.send(str(mod_blind).encode())
s_mod_msg_alice =str(mod_msg_alice).encode()

s.sendall(s_mod_msg_alice)

c_msg3 = str(s.recv(1024))

s_msg3 = ''
for i in c_msg3:
	if(i != 'b' and i != '\''):
		s_msg3 = s_msg3 + i
		
print(s_msg3)
print()


##Blind Signature Step
blind_a = ((s.recv(1024).decode()))
print("Blindly signed Message recieved from Bank: ",blind_a)
s.sendall(b'Blind Signature is done.')
print()


##Actual Signature for message

act_sign = generate_sign(blind_a,x_alice)

print("Actual Signature of Alice: (",r, ",",act_sign," )")
print()


##Verification of Signature using ElGamal Property

Verifier(act_sign)
etime = time.time()
if(choice == 1):
	fhand2 = open('proposed.txt','a+')
	cal_time = etime - stime
	s_time = " " + str(cal_time)
	fhand2.write(s_time)


s.close()

