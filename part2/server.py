import sys
import socket
import datetime

#get myport parentip parentport ipsfilename

myPort = sys.argv[1]
parentIP = sys.argv[2]
parentPort = sys.argv[3]
ipsFileName = sys.argv[4]
dictionary = {}
start_time = datetime.datetime.now().timestamp()

def loadFile(nameFile):
	with open(nameFile, "r") as file:
		for line in file:
			splitLine = line.split(",", 1)
			add = { splitLine[0] : splitLine[1] }
			dictionary.update(add)
	file.close()

def deleteVal(nameFile):
	file = open(nameFile, "r+")
	file.truncate()
	for key in dictionary.keys():
		file.write(key)
		file.write("," + dictionary.get(key))
	file.close()

def learnVal(nameFile):
	with open(nameFile, "a") as file:
		file.write("\n")
		file.write(inf)
		file.write(",")
		file.write(dictionary.get(inf))
	file.close()

loadFile(ipsFileName)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(myPort)))

while True:
	data, addr = s.recvfrom(1024)
	inf = data.decode()
	if (inf in dictionary.keys()):
		val = dictionary.get(inf)
		splitVal = val.split(",", 1)
		if (start_time > int(splitVal[1])):
			dictionary.pop(inf) #delete from the dictionary
			deleteVal(ipsFileName)
		s.sendto(val.encode() ,addr)

	else: #check in the parent file
		parentSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		parentSocket.sendto(inf.encode(), (parentIP, int(parentPort)))
		newdata, newaddr = parentSocket.recvfrom(1024)
		s.sendto(newdata ,addr)
		newAdd = {inf : newdata.decode()} #add to dictionary
		dictionary.update(newAdd)
		learnVal(ipsFileName) #update the origin file
		parentSocket.close()



