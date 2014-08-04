from wordnik import *


def dictdefine(word):
    replacedword = word.strip()
    apiUrl = 'http://api.wordnik.com/v4'
    apiKey = '98f47f77bcf4336a25002080d1e075ac9dd8751b07bc2eb54'
    client = swagger.ApiClient(apiKey, apiUrl)

    wordApi = WordApi.WordApi(client)
    dictdefined = wordApi.getDefinitions(replacedword)

    return dictdefined


def define(ircclientinstance, serverbuffer):
    commandname = 'define'
    commands = {':!': False, ':.': False, ':@': False}
    output = []
    notfound = "No info found :3"
    commandarguements = ""
    parseargs = serverbuffer[3:][1:]

    for x in parseargs:
        commandarguements += x.strip() + " "

    if commandarguements == '':
        output.append(notfound)
    else:
        try:
            dcontents = dictdefine(commandarguements)
            output.append("[\x033Define\x03]: %s" % dcontents[0].text)
        except:
            output.append(notfound)

    if serverbuffer[3][2:] == commandname:
        if serverbuffer[3][:2] in commands:
            notice = commands.get(serverbuffer[3][:2])

            if not notice:
                if serverbuffer[1] == "privmsg":
                    if serverbuffer[2] in ircclientinstance.ircchanlist:
                        for line in output:
                            ircclientinstance.sendmessage(
                                serverbuffer[2], line)
                    else:
                        for line in output:
                            ircclientinstance.sendmessage(
                                ircclientinstance.getusernick(serverbuffer), output)
            else:
                for line in output:
                    ircclientinstance.sendnotice(
                        ircclientinstance.getusernick(serverbuffer), output)
