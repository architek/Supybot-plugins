import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Repology')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Repology', True)


Repology = conf.registerPlugin('Repology')

conf.registerGroup(Repology, 'defaults')
conf.registerGlobalValue(Repology.defaults, 'distros',
    registry.String("{}", _("""The JSON structure of prefered distro
    per user.""")))
conf.registerGlobalValue(Repology.defaults, 'display',
    registry.String("gentoo,arch,debian_unstable,debian_stable,ubuntu_18_04",
    _("""The default list of distro to display.""")))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
