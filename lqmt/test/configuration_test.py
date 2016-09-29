from lqmt.lqm.systemconfig import SystemConfig
from lqmt.test.sample_config import USERCONFIG
from lqmt.lqm.config import LQMToolConfig
from unittest import TestCase, main
import os


class TestConfiguration(TestCase):
    """
    Testing class for the configuration components
    """

    def setUp(self):
        """
        Initialize the system configuration and the user configuration.

        Note the forward slash replacements for the user configuration. This is due to the forward slash being a
        restricted character in TOML(package used to parse configuration files in LQMT).
        """
        # relative pathing variables
        self.directory = os.path.dirname(__file__)
        self.alerts = self.directory + "\\test-data\\test-alerts"
        self.alerts = self.alerts.replace("\\", "\\\\")
        self.logging = self.directory + "\\test-data\\test-logs\\lqmt"
        self.logging = self.logging.replace("\\", "\\\\")
        self.whitelist = self.directory + "\\test-data\\whitelist\\whitelist.txt"
        self.whitelist = self.whitelist.replace("\\", "\\\\")
        self.whitelist_db = self.directory + "\\test-data\\whitelist\\whitelist.db"
        self.whitelist_db = self.whitelist_db.replace("\\", "\\\\")

        # configurations initialized.
        sysconf = SystemConfig()
        self.sys_config = sysconf.getConfig()
        config = USERCONFIG.format(self.alerts, self.logging, self.whitelist, self.whitelist_db)
        self.user_config = LQMToolConfig(config)

    def test_user_sources(self):
        """
        Note the replace call. The alert path was replaced with 4 slashes above due to a TOML restriction. After TOML
        parses the config defined above, it strips the extra slashes. We have to do that with our non-stripped alerts
        variable
        """
        sources = self.user_config.getSources().pop()
        self.assertEquals(sources._dirs, [self.alerts.replace("\\\\", "\\")])
        self.assertIsNone(sources.files_to_process)

    def test_user_whitelist(self):
        whitelist = self.user_config.getWhitelist()
        self.assertIsNotNone(whitelist)
        self.assertEqual(whitelist.whitelistFile, self.whitelist.replace("\\\\", "\\"))
        self.assertEqual(whitelist.db, self.whitelist_db.replace("\\\\", "\\"))

    def test_user_parsers(self):
        self.assertIsNotNone(self.user_config.getParser('Cfm13Alert'))
        self.assertIsNotNone(self.user_config.getParser('Cfm20Alert'))
        self.assertIsNotNone(self.user_config.getParser('stix-tlp'))

    def test_user_toollist(self):
        self.assertEqual(self.user_config.getToolsList(), ['FlexText'])

    def test_user_toolchain(self):
        toolchain = self.user_config.getToolChains().pop()
        self.assertEquals(toolchain._name, "anl-flextext-test")
        self.assertEquals(len(toolchain._tools), 1)

if __name__ == '__main__':
    main()
