import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircdb as ircdb
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

from requests import (get, HTTPError)
from collections import defaultdict
import json

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Repology')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class Repology(callbacks.Plugin):
    """Repology.org scrapper"""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Repology, self)
        self.__parent.__init__(irc)

    def repversion(self, irc, msg, args):
        """

        Returns the Repology plugin version
        """
        irc.reply("Repology 0.6")
    repversion = wrap(repversion)

    def pref(self, irc, msg, args, distro, user):
        """<[distro]> <[user]>
        Get or set user preference for distro(s) to display.
        Setting distro as "" will remove all prefs for user
        """
        try:
            cuser = ircdb.users.getUser(msg.prefix)
            if user:
                username = user
            else:
                username = cuser.name
 
            # Owner gets a private message with all prefs
            isOwner = cuser._checkCapability('owner')

            # Only Owner
            if user and not isOwner:
                irc.error("You don't have the owner capability to set a user distro preferences")
                return
 
            # Get distro database
            d = json.loads(self.registryValue('defaults.distros'))

            if distro is not None:
                if distro:
                    # Set prefs for user
                    d[username] = distro.split(',')
                else:
                    # Clear prefs
                    d.pop(username,None)
                self.setRegistryValue('defaults.distros', value=json.dumps(d))
                irc.replySuccess()
                return
            elif isOwner:
                irc.reply("Default distro Database: " + str(d), private=True)
                return
            else:
                res = "Default distro for %s set to %s" % (username, str(d[username]))
        except ValueError:
            irc.error('List of distros needs to be corrected. Please contact the bot admin.')
            self.log.error("List of distro needs to be fixed using config config supybot.plugins.Repology.defaults.distros")
            self.log.error("Current list is not a correct json message : " + self.registryValue('defaults.distros'))
            return
        except KeyError:
            irc.reply('I don\'t recognize you.')
            return
 
        irc.reply(res)
    pref = wrap(pref, [optional('anything'),optional('nick')])

    def rep(self, irc, msg, args, software, distro):
        """<software name> [<distro>|all]
        Search repology.org for software in the following repo:
        From the given distro parameter OR
        From user preferences if set OR
        From common distros configured if no preference found or distro parameter is "all"
        """

        # Default distro list
        wanted_distro = self.registryValue('defaults.display').split(",")

        try:
            user = ircdb.users.getUser(msg.prefix)
            username = user.name
        except KeyError:
            username = ""

        payload = {}
        if distro:
            payload["inrepo"] = distro  # No effect. Repology.org doesn't seem to work as documented ?
            if distro != "all":
                wanted_distro = distro
        else:
            # Get distro database
            try:
                d = json.loads(self.registryValue('defaults.distros'))
                if username and username in d.keys() and d[username] != ["all"]:
                    wanted_distro = d[username]
            except ValueError:
                # Database needs to be fixed
                self.log.error("List of distro needs to be fixed using config config supybot.plugins.Repology.defaults.distros")
                self.log.error("Current list is not a correct json message : " + self.registryValue('defaults.distros'))
                pass
        try:
            query = "https://repology.org//api/v1/metapackage/%s" % software
            r = get(query, params=payload)
            r.raise_for_status()
            vers = defaultdict(dict)
            for dist in r.json():
                repo = dist["repo"]
                ver = dist["version"]
                if repo in wanted_distro:
                    vers[repo][ver] = True

        except HTTPError:
            irc.error("http status %s" % r.status_code)
            return
        except ValueError:
            irc.error('Invalid Json response from repology')
            return
        except Exception as e:
            irc.error("Error occured while executing search [%s]: Http Status [%s]" % (e, r.status_code))
            return

        res = software + ": "
        for dist, ver in sorted(vers.items()):
            #res += dist + " ► " + ", ".join(sorted(ver.keys())) + " | "
            res += ("%s ► %s | " % (ircutils.bold(dist), ", ".join(sorted(ver.keys()))))
        if vers:
            irc.reply(res[:-3])
        else:
            irc.reply(res + "None")
    rep = wrap(rep, ['something', optional('something')])


Class = Repology

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
