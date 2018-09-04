import time
from supybot import utils, plugins, ircutils, callbacks
import supybot.ircdb as ircdb
from collections import defaultdict
from confusable_homoglyphs import confusables
from supybot.commands import *

class Unidet(callbacks.Plugin):
    """
    Detect spam using mix of different unicode classes. This is often used to fool bad words detectors.
    Threshold above which the bot will kick user is configurable. Defaults to 3 allowed mixed unicode classes every 60s.
    """
    def __init__(self, irc):
        self.__parent = super(Unidet, self)
        self.__parent.__init__(irc)
        self.thresh = defaultdict(list)
        self.active = True

    def callCommand(self, name, irc, msg, *args, **kwargs):
        if ircdb.checkCapability(msg.prefix, 'admin'):
            self.__parent.callCommand(name, irc, msg, *args, **kwargs)
        else:
            irc.errorNoCapability('admin')

    def inFilter(self, irc, msg):
        if msg.command == 'PRIVMSG' and self.active:
            channel = msg.args[0]
            s = ircutils.stripFormatting(msg.args[1])
            if ircutils.isChannel(channel) and self.registryValue('kick', channel):
                if confusables.is_mixed_script(s):
                    c = irc.state.channels[channel]
                    cap = ircdb.makeChannelCapability(channel, 'op')
                    u = msg.nick

                    t = time.time()
                    self.thresh[u].append(t)
                    self.thresh[u] = [ item for item in self.thresh[u] if item>(t-self.registryValue('slw')) ]

                    self.log.warning("Detected mixed <%s>, threshold"
                                "for user %s is now %s",s, u, len(self.thresh[u]))
                    if len(self.thresh[u]) > self.registryValue('rep'):
                        self.log.warning("Threshold reached, trying to kick %s", u)
                        if c.isHalfopPlus(irc.nick):
                            if c.isHalfopPlus(u) or \
                                    ircdb.checkCapability(msg.prefix, cap):
                                self.log.warning("Not kicking %s from %s, because "
                                           "they are halfop+ or can't be "
                                           "kicked.", u, channel)
                            else:
                                message = self.registryValue('kick.message', channel)
                                irc.queueMsg(ircmsgs.kick(channel, u, message))
                                self.log.warning("Kicked %s from %s", u, channel)
                        else:
                            self.log.warning('Should kick %s from %s, but not opped.',
                                             u, channel)
        return msg

Class = Unidet

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
