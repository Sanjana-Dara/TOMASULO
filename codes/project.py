import collections
import itertools
import threading
import random
import time
import os
from time import sleep
import subprocess

#memory
mem = [1 , 2 , 4 , 2 , 6, 5]

time_taken = { }

#Initialize values of Floating Point registers(assuming there are 10 registers)
fp = {
	"F0" : 23,
	"F1" : 6,
	"F2" : 12, 	 
	"F3" : 10,	
	"F4" : 12,  
	"F5" : 6,
	"F6" : 5,
	"F7" : 0,
	"F8" : 2,
	"F9" : 1
}

#Initialize values of Address Registers registers(assuming there are 5 registers)
ar = {
	"R0" : -1 ,
	"R1" : -5 ,
	"R2" : 25 ,
	"R3" : -10 ,
	"R4" : 40
}

#Number of Functional Units
Adders = 3
Subs = 2
Multiplers = 2
Div = 2
Lunits = 2

#Maintains which registers are busy
busy = []
busy1 = []
busy2 = []
busy3 = []

#Number of processes in each unit
process1 = []
process2 = []
process3 = []

acount = 0
scount = 0
mcount = 0
dcount = 0
lcount = 0
clk1=0
clk2=0
clk3=0

log = ["AND","NAND","OR","NOR","XOR","XNOR","NOT","RSH","LSH"]



busyx=[]
global mlck
mclk=0
global count
count=1

ins_1=[]

clockcycles={}
stages=[]

lock1 = threading.Semaphore()
lock2 = threading.Semaphore()
lock3 = threading.Semaphore()
lock4 = threading.Semaphore()

fileName = input("Enter the File name: ")
f = open(fileName,"r")

clockcycles ={}
stages=[]
instruction = []


Icount = 0
print("MEMORY:",mem)
print("FP REGS:",fp)
print("ADRESS REGS:",ar)
print("-----------------------")
for line in f:	
	line = line.rstrip().lstrip()
	if(line == "end"):
		break
	print(line)
	instruction.append(line)
print("-----------------------\n")
f.close()

Instruction = collections.namedtuple('Instruction', ('opcode', 'write_register', 'read_registers'))
for i in range(len(instruction)):
	stages.append({"fetch":0, "execute":0, "writeback":0})
#finishtime = { "ADD" : 6,"SUB" : 6,"MUL" : 10,"DIV" : 2,"LDR" : 2,"STR" : 2,"AND" : 2,"NAND" : 2,"NOT" :2,"XOR" : 2,"XNOR": 2,"OR : 2", "NOR":2,"LSH" : 2,"RSH" :2}
finishtime={}

def registerseperator(ins):
	ins_1 = []
	ins_1.append(ins[1])
	for j in range(len(ins[2])):
		ins_1.append(ins[2][j])
	return ins_1	

def addition(i,ins,start,Ccount,clk1):
	print("\n",Ccount," ",ins[0])
	print("\nREAD REG1",ins[2][0],":",fp[ins[2][0]],"\nREAD REG2",ins[2][1],":",fp[ins[2][1]])
	ans = 0
	
	for j in ins[2]:
		n = "{:064b}".format(ans)
		p = "{:064b}".format(fp[j])
		a = "a="+str(n)
		b = "b="+str(p)
		path = "./64adder +" + a + " +" + b +" +cin=0"
		x = subprocess.check_output(path,shell=True)
		y = str(x)
		y = y.replace(" ","")
		z = y.split('\'')[1].split('\'')[0].rstrip('\\n').split(",")[0].split('=')[1]
		ans = int(z)
	time_taken[Ccount].append(time.time())
	
	
	time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	lock3.acquire()
	fp[ins[1]] = ans
	lock3.release()
	time_taken[Ccount].append(time.time())
	print(" ADD WRITE REG",ins[1],":",fp[ins[1]])
	clockcycles[Ccount]=clk1+6

def subtraction(i,ins,start,Ccount,clk1):
	print("\n",Ccount," ",ins[0])
	print("\nREAD REG1",ins[2][0],":",fp[ins[2][0]],"\nREAD REG2",ins[2][1],":",fp[ins[2][1]])
	tmp = ins[2]
	
	ans = fp[tmp[0]]
	
	for j in tmp[1:]:
		n1 = "{:064b}".format(ans)
		p1 = "{:064b}".format(fp[j])
		a1 = "a="+str(n1)
		b1 = "b="+str(p1)
		path1 = "./sub64 +" + a1 + " +" + b1 +" +cin=1"
		x1 = subprocess.check_output(path1,shell=True)
		y1 = str(x1)
		y1 = y1.replace(" ","")
		z1 = y1.split('\'')[1].split('\'')[0].rstrip('\\n').split(",")[0].split('=')[1]
		ans = int(z1)
		# ans -= fp[j]
	time_taken[Ccount].append(time.time())
	time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	lock3.acquire()
	fp[ins[1]] = ans
	lock3.release()
	time_taken[Ccount].append(time.time())
	clockcycles[Ccount]=clk1+6
	print("SUB WRITE REG",ins[1],":",fp[ins[1]])

def multiplication(i,ins,start,Ccount,clk2):
	print("\n",Ccount," ",ins[0])
	print("\nREAD REG1",ins[2][0],":",fp[ins[2][0]],"\nREAD REG2",ins[2][1],":",fp[ins[2][1]])
	ans = 1
	
	for j in ins[2]:
		n = "{:016b}".format(ans)
		p = "{:016b}".format(fp[j])
		a = "a="+str(n)
		b = "b="+str(p)
		path = "./mul16 +" + a + " +" + b
		x = subprocess.check_output(path,shell=True)
		y = str(x)
		y = y.replace(" ","")
		z = y.split('\'')[1].split('\'')[0].rstrip('\\n').split(",")[0].split('=')[1]
		ans = int(z)
		# ans *= fp[j]
	time_taken[Ccount].append(time.time())
	time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	lock3.acquire()
	fp[ins[1]] = ans
	lock3.release()
	time_taken[Ccount].append(time.time())
	clockcycles[Ccount]=clk2+10
	print("MUL WRITE REG",ins[1],":",fp[ins[1]])

def division(i,ins,start,Ccount,clk2):
	print("\n",Ccount," ",ins[0])
	tmp = ins[2]
	ans = fp[tmp[0]]/fp[tmp[1]]
	time_taken[Ccount].append(time.time())
	time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	lock3.acquire()
	fp[ins[1]] = ans
	lock3.release()
	time_taken[Ccount].append(time.time())
	print("\nREAD REG1",ins[2][0],":",fp[ins[2][0]],"\nREAD REG2",ins[2][1],":",fp[ins[2][1]],"\nWRITE REG",ins[1],":",fp[ins[1]])	
	clockcycles[Ccount]=clk2+2
  

def logical(i,ins,start,Ccount,clk3):
	print("\n",Ccount," ",ins[0])
	global x,y
	tmp = ins[2]
	if(isinstance(tmp[0],int)):
		ans = tmp[0]
	else:
		ans = fp[tmp[0]]
	x=fp[ins[2][0]]
	y=fp[ins[2][1]]
	if(ins[0] == "AND"):
		for j in tmp[1:]:
			if(isinstance(j,int)):
				ans = ans & j
			else:
				ans = ans & fp[j]  
		time_taken[Ccount].append(time.time())
		time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	if(ins[0] == "OR"):
		for j in tmp[1:]:
			if(isinstance(j,int)):
				ans = ans | j
			else:
				ans = ans | fp[j]
		time_taken[Ccount].append(time.time())
		time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	if(ins[0] == "XOR"):
		for j in tmp[1:]:
			if(isinstance(j,int)):
				ans = ans ^ j
			else:
				ans = ans ^ fp[j] 
		time_taken[Ccount].append(time.time())
		time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	if(ins[0] == "NAND"):
		for j in tmp[1:]:
			if(isinstance(j,int)):
				ans = ~(ans & j)
			else:
				ans = ~(ans & fp[j])
		time_taken[Ccount].append(time.time())
		time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	if(ins[0] == "NOR"):
		for j in tmp[1:]:
			if(isinstance(j,int)):
				ans = ~(ans | j)
			else:
				ans = ~(ans | fp[j])
		time_taken[Ccount].append(time.time())
		time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	if(ins[0] == "XNOR"):
		for j in tmp[1:]:
			if(isinstance(j,int)):
				ans = ~(ans ^ j)
			else:
				ans = ~(ans ^ fp[j])
		time_taken[Ccount].append(time.time())
		time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	if(ins[0] == "LSH"):
		for j in tmp[1:]:
			if(isinstance(j,int)):
				ans = ans << j
			else:
				ans = ans << fp[j]
		time_taken[Ccount].append(time.time())
		time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	if(ins[0] == "RSH"):
		for j in tmp[1:]:
			if(isinstance(j,int)):
				ans = ans >> j
			else:
				ans = ans >> fp[j]
		time_taken[Ccount].append(time.time())
		time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	if(ins[0] == "NOT"):
		ans = ~(fp[tmp[0]]) 
		time_taken[Ccount].append(time.time())
		time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	lock3.acquire()
	fp[ins[1]] = ans
	lock3.release()
	time_taken[Ccount].append(time.time())
	print("READ REG1",ins[2][0],":",x,"\nREAD REG2",ins[2][1],":",y,"\nWRITE REG",ins[1],":",fp[ins[1]])
	clockcycles[Ccount]=clk3+2


def load(i,ins,start,Ccount,clk3):
	print("\n",Ccount," ",ins[0])
	
	val = int(ins[2][0]) + ar[ins[2][2]]
	time_taken[Ccount].append(time.time())
	time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	lock3.acquire()
	fp[ins[1]] = mem[val%6]
	lock3.release()
	time_taken[Ccount].append(time.time())
	print("Read address:",ins[2],"\nMem value in read address:",mem[val%6],"\nLoaded value in",ins[1],":", fp[ins[1]])
	clockcycles[Ccount]=clk3+2


def store(i,ins,start,Ccount,clk3):
	print("\n",Ccount," ",ins[0])
	val = int(ins[1]) + ar[ins[2][1]]
	time_taken[Ccount].append(time.time())
	time_taken[Ccount].append(time_taken[Ccount][1]-time_taken[Ccount][0])
	lock3.acquire()
	mem[val%6] = fp[ins[2][2]]
	lock3.release()
	time_taken[Ccount].append(time.time())
	print("Address in register",ins[2][1],":",ar[ins[2][1]],"\nWrite address:",val,"\nRead REG",ins[2][2],":",fp[ins[2][2]],"\nMem value in write address:",mem[val%6],)
	clockcycles[Ccount]=clk3+2
       

def InstructionCreator(string):
	# print("string  ",string)
	tokens = string.split(' ')
	opcode = tokens[0]
	write = tokens[1]
	read = []
	for i in range(2, len(tokens)):
		read.append(tokens[i])
	read = tuple(read)
	newInstr = Instruction(opcode=opcode, write_register=write, read_registers=read)
	return newInstr

def clockCycle1():
	global acount,scount,instruction,process1,busy,busy1,Icount,ins_1,clk1
	tmp = []
	length = len(instruction)
	prev = ""
	current = ""
	for i in range(length):
		newInstr = InstructionCreator(instruction[i])
		current = newInstr[0]
		if(i == 0):
			prev = newInstr[0]
		if(prev!=current):
			break
		ins_1 = registerseperator(newInstr)
		
		
		if(newInstr[0]=="ADD" and acount<3 and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			acount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy1.append(newInstr[j])
			start = time.time()
			thread = threading.Thread(target=addition, args=(i,newInstr,start,Ccount,clk1,))
			process1.append(thread)
			tmp.append(i)
		elif(newInstr[0]=="SUB" and scount<2 and any(item in newInstr for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			scount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy1.append(newInstr[j])
			start = time.time()
			thread = threading.Thread(target=subtraction, args=(i,newInstr,start,Ccount,clk1,))
			process1.append(thread)
			tmp.append(i)

	for ele in sorted(tmp,reverse = True):
		del instruction[ele]

def loop1():
	global acount,scount,instruction,process1,busy,busy1,Icount
	while(len(instruction)>0):
		lock1.acquire()
		
		clockCycle1()
		lock1.release()
		for thread in process1:
			thread.start()
			
		for thread in process1:
			thread.join()
		scount = 0
		acount = 0
		process1 = []
		lock2.acquire()
		busy_13 = [ele for ele in busy1 if ele in busy3]
		busy_12 =[ele for ele in busy1 if ele in busy2]
		busy = [ele for ele in busy if ele not in busy1]
		for i in range(len(busy_13)):
			busy.append(busy_13[i])
		for i in range(len(busy_12)):
			busy.append(busy_12[i])	
		lock2.release()

		

def clockCycle2():
	global mcount,dcount,instruction,process2,busy,busy2,Icount,ins_1,clk2
	
	tmp = []
	prev = ""
	current = ""
	for i in range(len(instruction)):
		newInstr = InstructionCreator(instruction[i])
		current = newInstr[0]
		if(i == 0):
			prev = newInstr[0]
		if(prev!=current):
			break
		ins_1=registerseperator(newInstr)
		clk2=clk2+1	
		if(newInstr[0]=="MUL" and mcount<2 and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			mcount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy2.append(newInstr[j])
			start = time.time()
			thread = threading.Thread(target=multiplication, args=(i,newInstr,start,Ccount,clk2,))
			process2.append(thread)
			tmp.append(i)
		elif(newInstr[0]=="DIV" and dcount<2 and any(item in newInstr for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			dcount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy2.append(newInstr[j])
			start = time.time()
			thread = threading.Thread(target=division, args=(i,newInstr,start,Ccount,clk2,))
			process2.append(thread)
			tmp.append(i)

	for ele in sorted(tmp,reverse = True):
		del instruction[ele]

def loop2():
	global mcount,dcount,instruction,process2,busy,busy2,Icount,busy_23,busy_12
	while(len(instruction)>0):
		lock1.acquire()
		
		clockCycle2()
		lock1.release()
		for thread in process2:
			thread.start()
			
		for thread in process2:
			thread.join()
		mcount = 0
		dcount = 0
		process2 = []
		lock2.acquire()
		busy_23 = [ele for ele in busy2 if ele in busy3]
		busy_12 =[ele for ele in busy2 if ele in busy1]
		busy = [ele for ele in busy if ele not in busy2]
		for i in range(len(busy_23)):
			busy.append(busy_23[i])
		for i in range(len(busy_12)):
			busy.append(busy_12[i])	
		lock2.release()


def clockCycle3():
	global lcount,instruction,process3,busy,busy3,Icount,ins_1,clk3
	tmp = []
	prev = ""
	current = ""
	for i in range(len(instruction)):
		newInstr = InstructionCreator(instruction[i])
		current = newInstr[0]
		if(i == 0):
			prev = newInstr[0]
		if(prev!=current):
			break
		ins_1=registerseperator(newInstr)
		clk3=clk3+1

		if(newInstr[0]=="OR" and lcount<2 and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			lcount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy3.append(newInstr[j])
			start = time.time()
			thread = threading.Thread(target=logical, args=(i,newInstr,start,Ccount,clk3,))
			process3.append(thread)
			tmp.append(i)
			lcount-=1
		elif(newInstr[0]=="XOR" and lcount<2 and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			lcount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy3.append(newInstr[j])
			start = time.time()

			thread = threading.Thread(target=logical, args=(i,newInstr,start,Ccount,clk3,))
			process3.append(thread)
			tmp.append(i)
			lcount-=1
		elif(newInstr[0]=="AND" and lcount<2 and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			lcount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy3.append(newInstr[j])
			start = time.time()

			thread = threading.Thread(target=logical, args=(i,newInstr,start,Ccount,clk3,))
			process3.append(thread)
			tmp.append(i)
			lcount-=1

		elif(newInstr[0]=="NAND" and lcount<2 and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			lcount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy3.append(newInstr[j])
			start = time.time()

			thread = threading.Thread(target=logical, args=(i,newInstr,start,Ccount,clk3,))
			process3.append(thread)
			tmp.append(i)
			lcount-=1

		elif(newInstr[0]=="NOR" and lcount<2 and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			lcount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy3.append(newInstr[j])
			start = time.time()

			thread = threading.Thread(target=logical, args=(i,newInstr,start,Ccount,clk3,))
			process3.append(thread)
			tmp.append(i)
			lcount-=1

		elif(newInstr[0]=="XNOR" and lcount<2 and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			lcount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy3.append(newInstr[j])
			start = time.time()

			thread = threading.Thread(target=logical, args=(i,newInstr,start,Ccount,clk3,))
			process3.append(thread)
			tmp.append(i)
			lcount-=1
		elif(newInstr[0]=="NOT" and lcount<2 and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			lcount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy3.append(newInstr[j])
			start = time.time()

			thread = threading.Thread(target=logical, args=(i,newInstr,start,Ccount,clk3,))
			process3.append(thread)
			tmp.append(i)
			lcount-=1

		elif(newInstr[0]=="LSH" and lcount<2 and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			lcount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy3.append(newInstr[j])
			start = time.time()

			thread = threading.Thread(target=logical, args=(i,newInstr,start,Ccount,clk3,))
			process3.append(thread)
			tmp.append(i)
			lcount-=1

		elif(newInstr[0]=="RSH" and lcount<2 and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			lcount+=1
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy3.append(newInstr[j])
			start = time.time()

			thread = threading.Thread(target=logical, args=(i,newInstr,start,Ccount,clk3,))
			process3.append(thread)
			tmp.append(i)

		elif(newInstr[0]=="LDR"  and any(item in ins_1 for item in busy)==False):
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			lock2.acquire()
			busy.append(newInstr[1])
			lock2.release()
			busy3.append(newInstr[1])
			start = time.time()

			thread = threading.Thread(target=load, args=(i,newInstr,start,Ccount,clk3,))
			process3.append(thread)
			tmp.append(i)
			lcount-=1

		elif(newInstr[0]=="STR"  and any(item in ins_1 for item in busy)==False):
			
			                       
			lock4.acquire()
			Icount+=1
			Ccount = Icount
			lock4.release()
			time_taken[Ccount] = [time.time()]
			for j in range(1,len(newInstr)):
				lock2.acquire()
				busy.append(newInstr[j])
				lock2.release()
				busy3.append(newInstr[j])
			start = time.time()
 
			thread = threading.Thread(target=store, args=(i,newInstr,start,Ccount,clk3,))
			process3.append(thread)
			tmp.append(i)
			lcount-=1


	for ele in sorted(tmp,reverse = True):
		del instruction[ele]

def loop3():
	global lcount,instruction,process3,busy,busy3,Icount
	while(len(instruction)>0):
		lock1.acquire()
		
		clockCycle3()
		lock1.release()
		for thread in process3:
			thread.start()
			
		for thread in process3:
			thread.join()
		lcount = 0
		process3 = []
		lock2.acquire()
		busy_23 = [ele for ele in busy3 if ele in busy2]
		busy_13 =[ele for ele in busy3 if ele in busy1]
		busy = [ele for ele in busy if ele not in busy3]
		for i in range(len(busy_23)):
			busy.append(busy_23[i])
		for i in range(len(busy_13)):
			busy.append(busy_13[i])	
		lock2.release()

		

thread1 = threading.Thread(target=loop1, args=())
thread2 = threading.Thread(target=loop2, args=())
thread3 = threading.Thread(target=loop3, args=())

thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()

f=open(fileName,"r")
for line in f:	
	line = line.rstrip().lstrip()
	if(line == "end"):
		break
	#print(line)
	instruction.append(line)
print("-----------------------\n")
f.close()

		
for i in range(len(instruction)):
	newInstr = InstructionCreator(instruction[i])
	#if (count==1):
		#mclk=mclk
	        #count=count-1
	#else:
	mclk=mclk+1
	stages[i]["fetch"]=mclk
	ins_1 = registerseperator(newInstr)
	
	#print(ins_1)
	if(newInstr[0]=="ADD" and acount<3 and any(item in ins_1 for item in busyx)==False):
		stages[i]["execute"]=mclk+6
		stages[i]["writeback"]=mclk+7
		
		finishtime[ins_1[0]]=mclk+6
		busyx.append(ins_1[0])
	elif(newInstr[0]=="ADD" and acount<3 and any(item in ins_1 for item in busyx)==True):
		
	  
		if ((ins_1[0] not in busyx)==False):
			if(finishtime[ins_1[0]]>mclk):
			
				stages[i]["execute"]=6+finishtime[ins_1[0]]
				stages[i]["writeback"]=7+finishtime[ins_1[0]]
			else:
				stages[i]["execute"]=mclk+6
				stages[i]["writeback"]=mclk+7
		if ((ins_1[1] in busyx)==True):
			if(finishtime[ins_1[1]]>mclk):
			
				stages[i]["execute"]=6+finishtime[ins_1[1]]
				stages[i]["writeback"]=6+finishtime[ins_1[1]]+1
			else:
				stages[i]["execute"]=mclk+6
				stages[i]["writeback"]=mclk+7
		if ((ins_1[2] in busyx)==True):
			if(finishtime[ins_1[2]]>mclk):
			
				stages[i]["execute"]=6+finishtime[ins_1[2]]
				stages[i]["writeback"]=6+finishtime[ins_1[2]]+1
			else:
				stages[i]["execute"]=mclk+6
				stages[i]["writeback"]=mclk+7
		
		busyx.append(ins_1[0])
		finishtime[ins_1[0]]=stages[i]["execute"]
		

	if(newInstr[0]=="SUB" and scount<3 and any(item in ins_1 for item in busyx)==False):
		stages[i]["execute"]=mclk+7
		stages[i]["writeback"]=mclk+8
		
		finishtime[ins_1[0]]=7+mclk
		busyx.append(ins_1[0])
	elif(newInstr[0]=="SUB" and scount<3 and any(item in ins_1 for item in busyx)==True):
		if ((ins_1[0] in busyx)==True):
			if(finishtime[ins_1[0]]>mclk):
			
				stages[i]["execute"]=7+finishtime[ins_1[0]]
				stages[i]["writeback"]=7+finishtime[ins_1[0]]+1
			else:
				stages[i]["execute"]=mclk+7
				stages[i]["writeback"]=mclk+8
		if ((ins_1[1] in busyx)==True):
			if(finishtime[ins_1[1]]>mclk):
			
				stages[i]["execute"]=7+finishtime[ins_1[1]]
				stages[i]["writeback"]=8+finishtime[ins_1[1]]
				
			else:
				stages[i]["execute"]=mclk+7
				stages[i]["writeback"]=mclk+8
		if ((ins_1[2] in busyx)==True):
			if(finishtime[ins_1[2]]>mclk):
			
				stages[i]["execute"]=7+finishtime[ins_1[2]]
				stages[i]["writeback"]=8+finishtime[ins_1[2]]
				
			else:
				stages[i]["execute"]=mclk+7
				stages[i]["writeback"]=mclk+8
		
		busyx.append(ins_1[0])
		finishtime[ins_1[0]]=stages[i]["execute"]
		
		 		 
	if(newInstr[0]=="MUL" and mcount<2 and any(item in ins_1 for item in busyx)==False):
		stages[i]["execute"]=mclk+10
		stages[i]["writeback"]=mclk+11
		mcount=mcount+1
		finishtime[ins_1[0]]=mclk+10
		busyx.append(ins_1[0])
	elif(newInstr[0]=="MUL" and mcount<3 and any(item in ins_1 for item in busyx)==True):
		if ((ins_1[0] in busyx)==True):
			if(finishtime[ins_1[0]]>mclk):
			
				stages[i]["execute"]=10+finishtime[ins_1[0]]
				stages[i]["writeback"]=11+finishtime[ins_1[0]]
				
			else:
				stages[i]["execute"]=mclk+10
				stages[i]["writeback"]=mclk+11
		if ((ins_1[1] in busyx)==True):
			if(finishtime[ins_1[1]]>mclk):
			
				stages[i]["execute"]=10+finishtime[ins_1[1]]
				stages[i]["writeback"]=11+finishtime[ins_1[1]]
			else:
				stages[i]["execute"]=mclk+10
				stages[i]["writeback"]=mclk+11
		if ((ins_1[2] in busyx)==True):
			if(finishtime[ins_1[2]]>mclk):
			
				stages[i]["execute"]=10+finishtime[ins_1[2]]
				stages[i]["writeback"]=11+finishtime[ins_1[2]]
			else:
				stages[i]["execute"]=mclk+10
				stages[i]["writeback"]=mclk+11
		
		busyx.append(ins_1[0])
		finishtime[ins_1[0]]=stages[i]["execute"]			
		
	if(newInstr[0]=="DIV" and dcount<3 and any(item in ins_1 for item in busyx)==False):
		stages[i]["execute"]=mclk+2
		stages[i]["writeback"]=mclk+3
		
		finishtime[ins_1[0]]=mclk+2
		busyx.append(ins_1[0])
	elif(newInstr[0]=="DIV" and dcount<3 and any(item in ins_1 for item in busyx)==True):
		if ((ins_1[0] in busyx)==True):
			if(finishtime[ins_1[0]]>mclk):
			
				stages[i]["execute"]=30+finishtime[ins_1[0]]
				stages[i]["writeback"]=31+finishtime[ins_1[0]]
				
			else:
				stages[i]["execute"]=mclk+30
				stages[i]["writeback"]=mclk+31
		if ((ins_1[1] in busyx)==True):
			if(finishtime[ins_1[1]]>mclk):
			
				stages[i]["execute"]=30+finishtime[ins_1[1]]
				stages[i]["writeback"]=31+finishtime[ins_1[1]]
			else:
				stages[i]["execute"]=mclk+30
				stages[i]["writeback"]=mclk+31
		if ((ins_1[2] in busyx)==True):
			if(finishtime[ins_1[2]]>mclk):
			
				stages[i]["execute"]=30+finishtime[ins_1[2]]
				stages[i]["writeback"]=31+finishtime[ins_1[2]]
			else:
				stages[i]["execute"]=mclk+30
				stages[i]["writeback"]=mclk+31
		
		busyx.append(ins_1[0])
		finishtime[ins_1[0]]=stages[i]["execute"]
			
	if((newInstr[0] in log) and lcount<3 and any(item in ins_1 for item in busyx)==False):
		stages[i]["execute"]=mclk+2
		stages[i]["writeback"]=mclk+3
		
		finishtime[ins_1[0]]=2+mclk
		busyx.append(ins_1[0])
	elif((newInstr[0] in log) and lcount<3 and any(item in ins_1 for item in busyx)==True):
		if ((ins_1[0] in busyx)==True):
			if(finishtime[ins_1[0]]>mclk):
			
				stages[i]["execute"]=2+finishtime[ins_1[0]]
				stages[i]["writeback"]=3+finishtime[ins_1[0]]
			else:
				stages[i]["execute"]=mclk+2
				stages[i]["writeback"]=mclk+3
		if ((ins_1[1] in busyx)==True):
			if(finishtime[ins_1[1]]>mclk):
			
				stages[i]["execute"]=2+finishtime[ins_1[1]]
				stages[i]["writeback"]=3+finishtime[ins_1[1]]
			else:
				stages[i]["execute"]=mclk+2
				stages[i]["writeback"]=mclk+3
		if ((ins_1[2] in busyx)==True):
			if(finishtime[ins_1[2]]>mclk):
			
				stages[i]["execute"]=2+finishtime[ins_1[2]]
				stages[i]["writeback"]=3+finishtime[ins_1[2]]
			else:
				stages[i]["execute"]=mclk+2
				stages[i]["writeback"]=mclk+3
		
		busyx.append(ins_1[0])
		finishtime[ins_1[0]]=stages[i]["execute"]		
		
		
	if(newInstr[0] == "LDR" and lcount<3 and any(item in ins_1 for item in busyx)==False):
		stages[i]["execute"]=mclk+2
		stages[i]["writeback"]=mclk+3
		
		finishtime[ins_1[0]]=2+mclk
		busyx.append(ins_1[0])
	elif(newInstr[0] == "LDR" and lcount<3 and any(item in ins_1 for item in busyx)==True):
		if ((ins_1[0] in busyx)==True):
			if(finishtime[ins_1[0]]>mclk):
			
				stages[i]["execute"]=2+finishtime[ins_1[0]]
				stages[i]["writeback"]=3+finishtime[ins_1[0]]
			else:
				stages[i]["execute"]=mclk+2
				stages[i]["writeback"]=mclk+3
		
		
		busyx.append(ins_1[0])
		finishtime[ins_1[0]]=stages[i]["execute"]
		
	if(newInstr[0] == "STR" and lcount<3 and any(item in ins_1 for item in busyx)==False):
		stages[i]["execute"]=mclk+2
		stages[i]["writeback"]=mclk+3
		
		finishtime[ins_1[0]]=2+mclk
		busyx.append(ins_1[0])
	elif(newInstr[0] == "STR" and lcount<3 and any(item in ins_1 for item in busyx)==True):
		if ((ins_1[3] in busyx)==True):
			if(finishtime[ins_1[3]]>mclk):
			
				stages[i]["execute"]=2+finishtime[ins_1[3]]
				stages[i]["writeback"]=3+finishtime[ins_1[3]]
			else:
				stages[i]["execute"]=mclk+2
				stages[i]["writeback"]=mclk+3
		
		busyx.append(ins_1[0])
		finishtime[ins_1[0]]=stages[i]["execute"]

for i in range(len(instruction)):
	print(stages[i],end="\t")
	print(instruction[i])
print("\nMEM:",mem)
print("FP REGS:",fp)
print("ADDRESS REGS:",ar)
#print(clockcycles)
print("\n\n#ins\tStart-time\t\tEnd-time\t\tExec-time\t\tWrite-back time")
for k in time_taken.keys():
	print(k,":", end="\t")
	for x in time_taken[k]:
		print(x,end = "\t")
	print("")
