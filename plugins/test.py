def test(ircclientinstance, serverbuffer):
    commandname = 'test'
    commands = {':!': True, ':.': False, ':@': False}
    output = "test"

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
