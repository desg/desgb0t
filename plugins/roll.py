import random

def roll(ircclientinstance,serverbuffer):
	commandname = 'roll'
	commands = {':!' : False, ':.' : False, ':@' : False}
	output = "[\x033rolled\x03] %s" % random.randint(0,100)

	if serverbuffer[3][2:] == commandname:
		if serverbuffer[3][:2] in commands:
			notice = commands.get(serverbuffer[3][:2])

			if not notice:
				if serverbuffer[1] == "privmsg":
						if serverbuffer[2] in ircclientinstance.ircchanlist:
							ircclientinstance.sendmessage(serverbuffer[2],output)
						else:
							sendernick = serverbuffer[0].split("!")
							sendernick = sendernick.replace(":","")
							ircclientinstance.sendmessage(sendernick,output)
			else:
				ircclientinstance.sendnotice(serverbuffer[2],output)