from supybot.test import *


class RepologyTestCase(PluginTestCase):
    plugins = ('Repology',)

    def testRepDef(self):
        self.assertNotError('rep 0ad')

    def testRepAll(self):
        self.assertNotError('rep 0ad all')

    def testGetPref(self):
        self.assertNotError('pref')

    def testSetPref(self):
        self.assertNotError('pref dist1,dist2')

    def testSetPrefUser(self):
        self.assertNotError('pref dist1,dist2 user')

    def testClearPref(self):
        self.assertNotError('pref "" user')

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
