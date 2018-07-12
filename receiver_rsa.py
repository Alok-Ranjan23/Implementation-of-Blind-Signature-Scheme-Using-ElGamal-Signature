import socket
import modu
import random
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



def msg_blind():
	
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
	
	msg_list = list()
	for i in msg:
		ch = ord(i)
		msg_list.append(ch)
	
	print()
	#print("Message_list: ",msg_list)
	
	#blind_factor
	global r
	r = random.randint(1,n)
	while(gcd(r,n) != 1):
		r = random.randint(1,n)
		
	print("Blind_Factor: ",r)
	print()
	
	blind_msg_list = list()
	for i in msg_list:
		j = modu.modular_exp(r,e,n)
		blind_msg_list.append((i*j)%n)
	
	#print("Blind_Message_list: ",blind_msg_list)
	print()
	
	blind_msg = ''
	for i in blind_msg_list:
		blind_msg = blind_msg + chr(i)
	
	return(blind_msg)



def retrieve_sign_msg(blind_signed_msg):
	
	blind_sign_list = list()
	for i in blind_signed_msg:
		j = ord(i)
		blind_sign_list.append(j)
		
	#print("Blind_sign_list: ",blind_sign_list)
	print()
	
	ri = modular_mul_inv(r,n)
	
	sign_list = list()
	for i in blind_sign_list:
		j = (i*ri)%n
		sign_list.append(j)
	
	#print("Actual Signed_list: ",sign_list)
	print()
	
	sign_msg = ''
	for i in sign_list:
		j = chr(i)
		sign_msg = sign_msg + j
	
	return(sign_msg)



def retrieve_message(signed_msg):
	
	signed_list = list()
	for i in signed_msg:
		j = ord(i)
		signed_list.append(j)
		
	msg_list = list()
	for i in signed_list:
		j = modu.modular_exp(i,e,n)
		msg_list.append(j)
	
	#print("Message List: ",msg_list)
	print()
	
	ret_msg = ''
	for i in msg_list:
		j = chr(i)
		ret_msg = ret_msg + j
	
	return(ret_msg)



s = socket.socket()
stime = time.time()
print("Socket Created Successfully")
print()

port = 12347

s.bind(('127.0.0.1',port))
print("Socket binded to %s"%(port))
print()

s.listen()
print("Socket is listening")
print()
c,addr = s.accept()
print("Got connection from: ",addr)
print()

global e
e = (str(c.recv(1024)))[2:-1]
e = int(e)
print(e)


c.send(b'Thank you for connecting')

global n
n = (str(c.recv(1024)))[2:-1]
n = int(n)
print(n)


mod_blind = msg_blind()

print("Blind_Msg: ",mod_blind)
print()
c.send(str(mod_blind).encode())

blind_signed_msg = c.recv(1024).decode()
print("Blind_signed_msg: ",blind_signed_msg)
print()
signed_msg = retrieve_sign_msg(blind_signed_msg)

print("Signture for actual message: ",signed_msg)
print()
ret_msg = retrieve_message(signed_msg)

print("Retrieved Message: ",ret_msg)
print()
if(ret_msg == msg):
	print("Chaum's Blind Signature is successfully done.")
else:
	print("Chaum's Blind Signature is not successfully done.")

etime = time.time()

if(choice == 1):
	fhand2 = open('chaum.txt','a+')
	cal_time = etime - stime
	s_time = " " + str(cal_time)
	fhand2.write(s_time)



c.close()



