from pystonk.api import Api

from unittest import TestCase
from mock import MagicMock, patch


class ApiTest(TestCase):
    def testInvalidAppKey(self):
        self.assertRaisesRegex(ValueError, 'Invalid App Key : ', Api, '', 'some_secret')
        self.assertRaisesRegex(ValueError, 'Invalid App Key : ', Api, '', '')

    def testInvalidAppSecret(self):
        self.assertRaisesRegex(ValueError, 'Invalid App Secret : ', Api, 'some_key', '')

    @patch('pystonk.api.requests')
    def testGetWrapperSuccess(self, requests_mock):
        response_mock = MagicMock()
        response_mock.json.return_value = {'foo': "bar"}
        requests_mock.get.return_value = response_mock

        o = Api('some key', 'some secret')
        t = o._get("some endpoint", params={'a': 1, 'b': 2})

        self.assertEqual(t, {'foo': "bar"}, "_get did not return expected data on success")

    @patch('pystonk.api.requests')
    def testPostWrapperSuccess(self, requests_mock):
        response_mock = MagicMock()
        response_mock.json.return_value = {'foo': "bar"}
        requests_mock.post.return_value = response_mock

        o = Api('some key', 'some secret')
        t = o._post("some endpoint", params={'a': 1, 'b': 2})

        self.assertEqual(t, {'foo': "bar"}, "_post did not return expected data on success")

    @patch('pystonk.api.requests')
    def testGetAccessTokenSuccess(self, requests_mock):
        response_mock = MagicMock()
        response_mock.json.return_value = {
            'expires_in': "3600",
            'token_type': "Bearer",
            'scope': "api",
            'access_token': "some token"}
        requests_mock.post.return_value = response_mock

        o = Api('some key', 'some secret')
        t = o.get_access_token()

        self.assertEqual(requests_mock.post.call_count, 1, "Mocked requests not called")
        self.assertEqual(t, "some token", "Api did not return expected access token when get_access_token is called")
        self.assertEqual(Api.ACCESS_TOKEN, "some token", "get_access_token did not set class property to expected value")

    @patch('pystonk.api.requests')
    def testGetAccessTokenFail(self, requests_mock):
        response_mock = MagicMock()
        response_mock.json.return_value = {}
        requests_mock.post.return_value = response_mock

        o = Api('some key', 'some secret')
        with self.assertRaises(ValueError):
            o.get_access_token()
        self.assertTrue("get_access_token failed to raise expected ValueError when access token is not found")
