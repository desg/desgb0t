import re
import requests

def unquote(url):
	return re.compile('%([0-9a-fA-F]{2})',re.M).sub(lambda m: chr(int(m.group(1),16)), url)

def rmUnwanted(string):
	string = string.replace("\n", " ")
	string = string.replace("<b>", "")
	string = string.replace("</b", "")

	return string

def lookup(search):
	search = search.replace(" ", "+")

	url = "https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s" % search

	headers = {'Referer' : 'xdesg.net'}


	rJson = requests.get(url, headers=headers).json()['responseData']['results']

	searchResults = []

	for result in rJson:
		searchResults.append({'url' : unquote(result['unescapedUrl']),
								'title' : rmUnwanted(result['title'])})

	return searchResults

def google(ircclientinstance,serverbuffer):
	commandname = 'google'
	commands = {':!' : True, ':.' : False, ':@' : False}
	commandarguements = ""

	parseargs = serverbuffer[3:][1:]

	for x in parseargs:
		commandarguements += x.strip() + " "

	if commandarguements == '':
		output = 'No info found :3'
	else:
		try:
			searchurl = lookup(commandarguements)[0]['url']
			output = "[\x033Google\x03]: Top google result for \"\x033%s\x03\": %s" % (commandarguements.strip(),searchurl)
		except:
			output = '[\x033Google\x03]: No info found :3 for "\x033%s\x03"' % commandarguements.strip()

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