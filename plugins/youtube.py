import requests
import datetime


def googlelookup(search):

    search.replace(" ", "+")

    apiurl = "https://gdata.youtube.com/feeds/api/videos?q=%s&alt=json" % search

    try:
        data = requests.get(apiurl).json()['feed']['entry']
        searchresults = []

        for entry in data:
            searchresults.append({'title': entry['title']['$t'].encode('utf-8'),
                                  'link': entry['link'][0]['href'],
                                  'author': entry['author'][0]['name']['$t'],
                                  'duration': entry['media$group']['yt$duration']['seconds'],
                                  'views': entry['yt$statistics']['viewCount']})
        return searchresults
    except KeyError:
        return None

# use this

def youtube(ircclientinstance, serverbuffer):
    commandname = ['yt', 'youtube']
    commands = {':!': True, ':.': False, ':@': False}
    commandarguements = ""

    parseargs = serverbuffer[3:][1:]

    for x in parseargs:
        commandarguements += x.strip() + " "

    if commandarguements == '':
        output = 'No info found :3'
    else:

        try:

            searchdata = googlelookup(commandarguements)[0]
            output = "[\x033Youtube\x03]: '\x033%s\x03' [\x033 %s\x03] uploaded by \x033%s\x03  | Views:\x033 %s\x03  | \x033%s\x03" %(
                searchdata['title'], 
                str(datetime.timedelta(0,int(searchdata['duration']))),
                searchdata['author'], searchdata['views'], searchdata['link'])

        except:
            output = 'No info found :3'

    if serverbuffer[3][2:] in commandname:
        if serverbuffer[3][:2] in commands:
            notice = commands.get(serverbuffer[3][:2])

            if not notice:
                if serverbuffer[1] == "privmsg":
                    if serverbuffer[2] in ircclientinstance.ircchanlist:
                        ircclientinstance.sendmessage(serverbuffer[2], output)
                    else:
                        ircclientinstance.sendmessage(
                            ircclientinstance.getusernick(serverbuffer), output)
            else:
                ircclientinstance.sendnotice(
                    ircclientinstance.getusernick(serverbuffer), output)
