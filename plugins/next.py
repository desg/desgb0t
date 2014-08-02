import requests

def showInfo(tvname):
    tvname = tvname.replace(' ', '+')
    tvinfo = requests.get("http://services.tvrage.com/tools/quickinfo.php?show=" + tvname).text
    try:
        tvdata = tvinfo.split('\n')
        tvinfo = []
        for data in tvdata:
            data = data.split('@')
            tvinfo.append(data)

        return tvinfo
    except:
        return None

def next(ircclientinstance,serverbuffer):
    commandname = 'next'
    commands = {':!' : True, ':.' : False, ':@' : True}

    # This needs to be included in all programs that take arguements
    commandarguements = ""
    parseargs = serverbuffer[3:][1:]

    for x in parseargs:
        commandarguements += x.strip() + " "

    if commandarguements == '':
        output = "No info found :3"
    else:
        try:
            tvinfo = showInfo(commandarguements)
            output = "[%s] :: [Next: %s] [Airs: %s]" % (tvinfo[1][1], tvinfo[7][1].replace('^', ' '), tvinfo[15][1])
        except:
             output = "No info found :3"

    # this needs to be included with all plugins
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