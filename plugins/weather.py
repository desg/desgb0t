import requests

def getweather(area):
	area = area.strip()
	area = area.replace(" ", "+")
	area = str(area)
	# TODO find out for what reason canadian zipcodes do not work
	apikey = "897522adf011af15"
	areaQuery = requests.get("http://autocomplete.wunderground.com/aq?query=%s" % area).json()

	searchData = areaQuery['RESULTS'][0]['l'] #Returns the first result

	jsonData = requests.get("http://api.wunderground.com/api/%s/conditions%s.json" % (apikey , searchData)).json()

	return jsonData

def weather(ircclientinstance,serverbuffer):
	commandname = 'weather'
	commands = {':!' : True, ':.' : False, ':@' : False}
	commandarguements = ""

	parseargs = serverbuffer[3:][1:]

	for x in parseargs:
		commandarguements += x.strip() + " "

	if commandarguements == '':
		output = 'No info found :3'
	else:

		try:
			weatherData = getweather(commandarguements)['current_observation']
			city = weatherData['display_location']['full']
			cWeather = weatherData['weather']
			temperature = weatherData['temperature_string']
			rHumidity = weatherData['relative_humidity']
			output = "%s [weather: %s][temperature: %s][relative humidity: %s]" % (city, cWeather, temperature, rHumidity)
		except:
			output = 'No info found :3'

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