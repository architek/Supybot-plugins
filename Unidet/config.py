from supybot import conf, registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Unidet')
except:
    _ = lambda x: x


def configure(advanced):
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Unidet', True)


Unidet = conf.registerPlugin('Unidet')

conf.registerChannelValue(Unidet, 'kick',
    registry.Boolean(False, _("""Determines whether the bot will kick people with
    a warning when they abuse confusable unicode.""")))

conf.registerGlobalValue(Unidet, 'slw',
    registry.Integer(60, _("""Sliding window in seconds.""")))

conf.registerGlobalValue(Unidet, 'rep',
    registry.Integer(3, _("""Repetition Filter.""")))

conf.registerChannelValue(Unidet.kick, 'message',
    registry.NormalizedString(_("""You have been kicked for using a word
    prohibited in the presence of this bot.  Please use more appropriate
    language in the future."""), _("""Determines the kick message used by the
    bot when kicking users for saying bad words.""")))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
