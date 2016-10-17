from cmd import cmds, save_conf, save_bullshit
import traceback

# dummy sender
class Sender(object):
    def __init__(self):
        self.name = 'Tester'
        self.id = 'DUMMY_MOD_ID'
sender = Sender()

# dummy receiver
class Receiver(object):
    def sendMessage(self, msg):
        print 'sendMessage: [%s]' % msg.encode('UTF-8')
    def sendImage(self, filename):
        print 'sendImage: [%s]' % filename.encode('UTF-8')
receiver = Receiver()

while True:
    try:
        msg = raw_input('in: ')
        cmd = msg.split()[0].lower()
        cmds[cmd](sender, msg, receiver)
    except KeyboardInterrupt:
        break
    except:
        save_bullshit(sender, msg)
        traceback.print_exc()
#save_conf()
