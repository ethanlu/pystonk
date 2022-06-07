from pystonk.commands.CommandHelp import CommandHelp

from unittest import TestCase


class CommandHelpTest(TestCase):
    def setUp(self) -> None:
        pass

    def testCommandHelpInstantiation(self):
        o = CommandHelp("SomeMadeUpCommand", "some description", "smu", [], [])

        self.assertEqual("Some Made Up", o.name, "CommandHelp did not instantiate with expected name format")
        self.assertEqual("smu", o.command, "CommandHelp did not instantiate with expected command format")
        self.assertEqual("some description", o.description, "CommandHelp did not instantiate with expected description format")
        self.assertListEqual([], o.required_parameters, "CommandHelp did not instantiate with expected required list")
        self.assertListEqual([], o.optional_parameters, "CommandHelp did not instantiate with expected optional list")
