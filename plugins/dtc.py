from datetime import date


def dtc(ircclientinstance, serverbuffer):
    commandname = 'dtc'
    commands = {':!': True, ':.': False, ':@': True}

    today = date.today()
    christmas = date(today.year, 12, 25)

    if christmas < today:
        christmas = christmas.replace(year=today.year + 1)

    tUntilChristmas = abs(christmas - today)

    output = "%i days until Christmas!" % tUntilChristmas.days

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
