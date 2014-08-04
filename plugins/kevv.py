import random

# returns a list of every line in log


def getListLog(filename):
    f = open(filename, 'r')

    ListLog = []
    for line in f:
        ListLog.append(line)

    return ListLog

# chooses a random name from from the nicks in filename


def choseRandomName(filename):
    listLog = getListLog(filename)
    namelist = []
    for name in listLog:
        newname = name.split(':')[0].replace('<', '').replace('>', '')
        if newname not in namelist:
            namelist.append(newname)
    return random.choice(namelist)

# chooses a random line from getListLog() with respect to name


def kevv(ircclientinstance, serverbuffer):
    commandname = 'kevv'
    commands = {':!': True, ':.': False, ':@': True}

    # TODO: programatically get filenamesup
    #filename = "%s.log" % ircclientinstance.getchannel(serverbuffer)
    filename = "#jeff.log"
    commandarguements = ""

    parseargs = serverbuffer[3:][1:]

    for x in parseargs:
        commandarguements += x.strip() + " "

    if commandarguements == '':
        name = choseRandomName(filename)
    else:
        name = commandarguements.strip()

    listLog = getListLog(filename)
    templist = []
    for line in listLog:
        if line.split(':')[0] == '<' + name + '>':
            templist.append(line)

    if len(templist) >= 1:
        randomLine = random.choice(templist)
        output = randomLine.replace(":", " ")
    else:
        output = None

    if serverbuffer[3][2:] == commandname:
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
