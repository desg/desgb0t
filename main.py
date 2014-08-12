import socket
import string
import sys
import os

path = "plugins/"
plugins = []
# Load plugins
sys.path.insert(0, path)
for f in os.listdir(path):
    fname, ext = os.path.splitext(f)
    if ext == '.py':
        mod = __import__(fname)
        plugins.append(getattr(mod, fname))
sys.path.pop(0)

class IRC_Client(object):

    """docstring for IRC_Client"""
    sock = ""

    def __init__(self, ircserver, ircnicklist, ircident, ircrealname,
                 ircchanlist, nickpassword=None, ircport=6667):
        super(IRC_Client, self).__init__()
        if not isinstance(ircnicklist, list):
            raise TypeError("nicklist is not an instance of list")
        elif not isinstance(ircchanlist, list):
            raise TypeError("chanlist is not an instance of list")

        self.ircnicklist = ircnicklist
        self.ircident = ircident
        self.ircrealname = ircrealname
        self.ircchanlist = ircchanlist
        self.ircserver = ircserver
        self.ircport = ircport
        self.nickpassword = nickpassword

    def create_connection(self):
        self.sock = socket.socket()
        self.sock.connect((self.ircserver, self.ircport))

    def sendmessage(self, sender, message):
        sent = "PRIVMSG %s :%s\r\n" % (sender, message)
        self.sock.send(sent)

    def send_pong(self, sender):
        sent = "PONG %s\r\n" % sender
        self.sock.send(sent)

    def sendnotice(self, sender, message):
        sent = "NOTICE %s :%s\r\n" % (sender, message)
        self.sock.send(sent)

    def sendctcp(self):
        pass

    def setnick(self, nick):
        self.sock.send("NICK %s\r\n" % nick)

    def joinchannel(self, channel):
        self.sock.send("JOIN %s\r\n" % channel)
    
    def getusernick(self, serverbuffer):
        usernick = serverbuffer[0].split("!")
        usernick = usernick[0].replace(":", "")
        return usernick

    def getusermessage(self, serverbuffer):
        message = ""
        if len(serverbuffer) >= 4:
            serverbuffer[3] == serverbuffer[3][1:]
            for i in range(3, len(serverbuffer)):
                message += serverbuffer[i] + " "
            return message

    def getchannel(self, serverbuffer):
        if len(serverbuffer):
            return serverbuffer[2]

    def serverreplies(self, serverbuffer):
        serverbuffer = tuple(string.split(string.rstrip(serverbuffer)))
        serv_responses = {"431": "ERR_NONICKNAMEGIVEN",
                        "432": "ERR_ERRONEUSNICKNAME",
                        "433": "ERR_NICKNAMEINUSE",
                        "442": "ERR_NOTONCHANNEL"}
        if serverbuffer[0] == "PING":
            self.send_pong(serverbuffer[0])


    def commandparser(self, line):
        line = string.split(string.rstrip(line.lower()))
        if (len(line) >= 4 and line[1] == 'privmsg') and (line[3].startswith(':@')
            or line[3].startswith(':!') or line[3].startswith(':.')):
            map(lambda command: command(self, line), plugins)


    def connect(self):
        self.create_connection()
        self.setnick(self.ircnicklist[0])
        self.sock.send("USER %s %s bla :%s\r\n"
                       % (self.ircident, self.ircserver, self.ircrealname))

        if self.nickpassword:
            self.sock.send("PASS %s\r\n" % self.nickpassword)

        for channel in self.ircchanlist:
            self.joinchannel(channel)

    def loop(self):

        readbuffer = ""
        while True:
            readbuffer = self.sock.recv(1024)
            temp = string.split(readbuffer, "\n")
            readbuffer = temp.pop()
            readbuffer = temp.pop().encode('utf-8')
            for line in temp:
                print line
                self.serverreplies(line)
                self.commandparser(line)
                logger(self, line)

    def runclient(self):

        self.connect()
        self.loop()


def logger(ircclientinstance, serverbuffer):

    serverbuffer = string.split(string.rstrip(serverbuffer))

    if serverbuffer[1].lower() == "privmsg":
        if serverbuffer[2] in ircclientinstance.ircchanlist:
            filename = ("%s.log" % serverbuffer[2])
            with open(filename, 'a+') as f:
                f.write("<%s>%s\n"
                % (ircclientinstance.getusernick(serverbuffer),
                    ircclientinstance.getusermessage(serverbuffer))) 
        else:
            filename = ("%s.log" % ircclientinstance.getusernick(serverbuffer))
            with open(filename, 'a+') as f:
                f.write("<%s>%s\n"
                % (ircclientinstance.getusernick(serverbuffer),
                    ircclientinstance.getusermessage(serverbuffer)))


if __name__ == "__main__":
    # TODO: config file? maybe
    mybot = IRC_Client('irc.swiftirc.net', ['swaglord', 'swaglordeh'], 'swaglorde', 
                    'swaglorde', ['#dtest'])
    mybot.run_client()
