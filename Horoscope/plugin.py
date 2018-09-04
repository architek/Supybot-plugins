import requests
import datetime
from ftfy import fix_encoding
from bs4 import BeautifulSoup
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from time import time, strftime, sleep


class Horoscope(callbacks.Plugin):
    """Horoscope
    To get the horoscope once at [00:00-01:00] localtime only:
    !scheduler repeat horo [seconds 59m] horo True"""
    threaded = True

    def horo(self, irc, msg, args, midnight_check, psign):
        """[bool: Only print when local hour is 0 - default False] [sign: if not set will dump all signs]
        Returns horoscope in french for one zodiacal sign or all
        """
        signs = []
        tsigns = ['belier', 'taureau', 'gemeaux', 'cancer', 'lion', 'vierge', 'balance', 'scorpion', 'sagittaire', 'capricorne', 'verseau', 'poissons']
        
        if midnight_check and int(datetime.datetime.fromtimestamp(time()).strftime('%H')):
            self.log.info("Horoscope plugin: checked and not [00:00-00:59] local time")
            return
        if psign:
            if psign not in tsigns:
                irc.error("Same player try again!")
            else:
                signs = [ psign ]
        else:
            signs = tsigns
        for sign in signs:
            url = "https://www.lhoroscope.com/horoscope-general/horoscope-%s-du-jour.asp" % sign
            try:
                result = requests.get(url)
                soup = BeautifulSoup(result.content)
                h = soup.find(class_="panel-body").text.strip()
                h = fix_encoding(h)
            except Exception as e:
                irc.error("Error {}".format(e))
                break
            else:
                irc.reply(ircutils.bold(sign.title()) + " : " + h, prefixNick=False)
            sleep(2)
    horo = wrap(horo, [optional('boolean'), optional('somethingWithoutSpaces')])


Class = Horoscope

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
