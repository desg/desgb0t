# -*- coding: utf-8 -*-

def trole(ircclientinstance,serverbuffer):
	commandname = 'trole'
	commands = {':!' : True, ':.' : False, ':@' : False}
	output = "( ͡° ͜ʖ ͡°)"

	if serverbuffer[3][2:] == commandname:
		if serverbuffer[3][:2] in commands:
			notice = commands.get(serverbuffer[3][:2])

			if not notice:
				if serverbuffer[1] == "privmsg":
						if serverbuffer[2] in ircclientinstance.ircchanlist:
							ircclientinstance.sendmessage(serverbuffer[2],output)
						else:
							ircclientinstance.sendmessage(ircclientinstance.getusernick(serverbuffer),output)
			else:
				ircclientinstance.sendnotice(ircclientinstance.getusernick(serverbuffer),output)