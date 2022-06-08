from pystonk.api import Api

from unittest import TestCase


class ApiTest(TestCase):
    def testInvalidApiKey(self):
        self.assertRaisesRegex(ValueError, 'Invalid API Key : ', Api, '')