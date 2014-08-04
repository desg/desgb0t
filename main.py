import socket
import string
import sys
import os

path = "plugins/"
plugins = []
#Load plugins
sys.path.insert(0, path)
for f in os.listdir(path):
    fname, ext = os.path.splitext(f)
    if ext == '.py':
        mod = __import__(fname)
        plugins.append(getattr(mod, fname))
sys.path.pop(0)

class IRC_Client(object):
	"""docstring for IRC_Client"""
	sock = ""
	def __init__(self,ircserver,ircnicklist,ircident,ircrealname,
					ircchanlist,nickpassword=None,ircport=6667):
		super(IRC_Client, self).__init__()
		if not isinstance(ircnicklist,list):
			raise TypeError("nicklist is not an instance of list")
		elif not isinstance(ircchanlist,list):
			raise TypeError("chanlist is not an instance of list")

		self.ircnicklist = ircnicklist
		self.ircident = ircident
		self.ircrealname = ircrealname
		self.ircchanlist = ircchanlist
		self.ircserver = ircserver
		self.ircport = ircport
		self.nickpassword = nickpassword

	def createconnection(self):
		self.sock = socket.socket()
		self.sock.connect((self.ircserver,self.ircport))

	def sendmessage(self,sender,message):
		sent = "PRIVMSG %s :%s\r\n" % (sender,message)
		self.sock.send(sent)

	def sendpong(self,sender):
		sent = "PONG %s\r\n" % sender
		self.sock.send(sent)

	def sendnotice(self,sender,message):
		sent = "NOTICE %s :%s\r\n" % (sender,message)
		self.sock.send(sent)

	def sendctcp(self):
		pass

	def setnick(self,nick):
		self.sock.send("NICK %s\r\n" % nick)

	def joinchannel(self,channel):
		self.sock.send("JOIN %s\r\n" % channel)

	def getusernick(self,serverbuffer):
		usernick = serverbuffer[0].split("!")
		usernick = usernick[0].replace(":", "")
		return usernick

	def getusermessage(self,serverbuffer):
		message = ""
		if len(serverbuffer) >=4:
			serverbuffer[3] == serverbuffer[3][1:]
			for i in range(3,len(serverbuffer)):
				message += serverbuffer[i] + " "
			return message

	def getchannel(self,serverbuffer):
		if len(serverbuffer):
			return serverbuffer[2]

	def serverreplies(self,serverbuffer):
		serverbuffer = string.split(string.rstrip(serverbuffer))

		if serverbuffer[0].lower() == 'ping':
			self.sendpong(serverbuffer[0])
		if serverbuffer[1] == "431":
			print "No nick was given"
			exit()
		if serverbuffer[1] == "432":
			print "Erroneus nick"
			exit()
		if serverbuffer[1] == "433":
			if len(self.ircnicklist) != 0:
				self.setnick(self.ircnicklist.pop())
			else:
				raise IndexError("All nicks from nicklist are in use")

			for channel in self.ircchanlist:
				self.joinchannel(channel)

	def connect(self):
		self.createconnection()
		self.setnick(self.ircnicklist[0])
		self.sock.send("USER %s %s bla :%s\r\n"
							% (self.ircident,self.ircserver,self.ircrealname))
		
		if not self.nickpassword:
			pass
		else:
			self.sock.send("PASS %s\r\n" % self.nickpassword)

		for channel in self.ircchanlist:
			self.joinchannel(channel)

def commandparser(ircclientinstance,serverbuffer):
	serverbuffer = string.split(string.rstrip(serverbuffer.lower()))

	if len(serverbuffer) >= 4 and serverbuffer[1] == 'privmsg':
	if (len(serverbuffer) >= 4 and serverbuffer[1] == 'privmsg' and 
		(serverbuffer[3].startswith(":@") or serverbuffer[3].startswith(":.") or 
		serverbuffer[3].startswith(":!"))):
		map(lambda command: command(ircclientinstance,serverbuffer),plugins)


# TODO: config file? maybe
mybot = IRC_Client('irc.freenode.net',['swaglorde','swaglordeh'],
					'swaglordeh','swaglordeh',['#dtest'])

def logger(ircclientinstance,serverbuffer):
	serverbuffer = string.split(string.rstrip(serverbuffer))

	if serverbuffer[1].lower() == "privmsg":
		if serverbuffer[2] in ircclientinstance.ircchanlist:
			filename = ("%s.log" % serverbuffer[2])
			f = open(filename, 'a+')
			f.write("<%s>%s\n" % (ircclientinstance.getusernick(serverbuffer),ircclientinstance.getusermessage(serverbuffer)))
			f.close()
		else:
			filename = ("%s.log" % ircclientinstance.getusernick(serverbuffer))
			f = open(filename, 'a+')
			f.write("<%s>%s\n" % (ircclientinstance.getusernick(serverbuffer),ircclientinstance.getusermessage(serverbuffer)))
			f.close()

def startbot(ircclientinstance,logging=True):
	ircclientinstance.connect()
	readbuffer = ""
	while 1:
		readbuffer += ircclientinstance.sock.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		for line in temp:
			ircclientinstance.serverreplies(line)
			commandparser(ircclientinstance,line)
			logger(ircclientinstance,line)
			print line

startbot(mybot)