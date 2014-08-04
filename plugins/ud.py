#!/usr/bin/python
# Author:ben from swiftirc
# urbandictionary.py
import lxml.html
import urllib2

api_url = 'http://www.urbandictionary.com/define.php?term=%s&page=%s'


def lookup(word, page=1):
    dom = lxml.html.fromstring(urllib2.urlopen(api_url % (word, page)).read())
    definitions = []
    entry_count = len(dom.xpath('//div[@class="ribbon"]'))
    for num in range(entry_count):
        definitions.append({'number':       dom.xpath('//div[@class="ribbon-inner"]')[num].text_content().strip()[:-1],
                            'word':         dom.xpath('//div[@class="word"]')[num].text_content().strip(),
                            'definition':   dom.xpath('//div[@class="meaning"]')[num].text_content().strip(),
                            'example':      dom.xpath('//div[@class="example"]')[num].text_content().strip()})

    return definitions


def lookup_number(word, number=1, page=1):
    definitions = lookup(word, page)
    if len(definitions) < number:
        number = len(definitions)
    return definitions[number - 1]


def lookup_abs_number(word, number=1):
    word = word.replace(" ", "+")
    page = number // 7 + 1
    number = number % 7
    return lookup_number(word, number, page)
# //end


def ud(ircclientinstance, serverbuffer):
    commandname = 'ud'
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
        # why do you crash me
        # @ud wanna see the #85 definition of brent describin him as a DICKHEAD
        # find another way to extract the number
        if "#" in commandarguements:

            commandarguements = commandarguements.strip()
            try:
                number = int(commandarguements[-1])
                definition = lookup_abs_number(commandarguements[:-1], number)
                output.append("[\x033UD\x03]: '\x033%s\x03' %s" %
                              (definition['word'], definition['definition']))
                output.append("[\x033Example\x03]: %s" % definition['example'])
            except:
                definition = lookup_abs_number(commandarguements)
                output.append("[\x033UD\x03]: '\x033%s\x03' %s" %
                              (definition['word'], definition['definition']))
                output.append("[\x033Example\x03]: %s" % definition['example'])
        else:
            try:
                definition = lookup_abs_number(commandarguements)
                output.append("[\x033UD\x03]: '\x033%s\x03' %s" %
                              (definition['word'], definition['definition']))
                output.append("[\x033Example\x03]: %s" % definition['example'])
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
                                ircclientinstance.getusernick(serverbuffer),
                                output)
            else:
                for line in output:
                    ircclientinstance.sendnotice(
                        ircclientinstance.getusernick(serverbuffer), output)
