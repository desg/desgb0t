from define import dictdefine

def storebwotd(bwotd):
    filename = "bwotd.txt"

    with open(filename, 'a+') as f:
        f.write(str(bwotd)+'\n')

def getbwotd():
    filename = "bwotd.txt"
    with open(filename, 'r') as f:
        wotd = f.readlines()[-1]

    wotd = wotd.split()
    word = wotd[1:]

    if wotd[0] == 'ud':
        # TODO: finish implementing this
        pass

    elif wotd[0] == 'define':
        dcontents = dictdefine("".join(word))
        if dcontents != None:
            this = "[\x033Define\x03]: '\x033%s\x03' %s" % ("".join(word), dcontents[0].text.encode('utf-8')) 
            return this
        return 'Word set not found'
    return 'test'


def bwotd(ircclientinstance, serverbuffer):
    commandname = 'bwotd'
    commands = {':!': True, ':.': False, ':@': False}
    commandarguements = ""
    # Burt's Word of The Day
    parseargs = serverbuffer[3:][1:]

    for x in parseargs:
        commandarguements += x.strip() + " "
    commandarguements = commandarguements.strip()
    commandlist = commandarguements.split()

    if len(commandlist) >= 1 and commandlist[0] == 'set':
        if (len(commandlist) >= 2 and 
            (commandlist[1] == 'ud' or commandlist[1] == 'define')):
            word = "%s %s" % (commandlist[1], " ".join(commandlist[2:]))
            output = 'bwotd set as: ', commandlist[2:]
            storebwotd(word)
        else:
            word = "define %s" % " ".join(commandlist[1:])
            storebwotd(word)
            output = 'bwotd set as: ', commandlist[1:]


    else:
        output = getbwotd()


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
