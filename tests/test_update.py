import base
from dnf.queries import \
    available_by_name, \
    installed_by_name, \
    updates_by_name

class Update(base.ResultTestCase):
    def test_update(self):
        """ Simple update. """
        yumbase = base.mock_yum_base("updates")
        ret = yumbase.update(pattern="pepper")
        new_versions = updates_by_name(yumbase.sack, "pepper")
        self.assertEqual(len(new_versions), 1)
        self.assertEqual([txmbr.po for txmbr in ret] , new_versions)
        self.assertResult(yumbase, new_versions + \
                              installed_by_name(yumbase.sack, "librita"))

    def test_update_not_installed(self):
        """ Updating an uninstalled package is a void operation. """
        yumbase = base.mock_yum_base("main")
        ret = yumbase.update(pattern="mrkite") # no "mrkite" installed
        self.assertEqual(ret, [])
        self.assertResult(yumbase,
                          installed_by_name(yumbase.sack, None))

    def test_update_all(self):
        """ Update all you can. """
        yumbase = base.mock_yum_base("main", "updates")
        sack = yumbase.sack
        ret = yumbase.update()
        expected = available_by_name(sack, "pepper", latest_only=True)
        self.assertItemsEqual((txmem.po for txmem in ret), expected)