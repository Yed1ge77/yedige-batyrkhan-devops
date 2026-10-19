"""Verify the Docker HTTP checker catches incorrect endpoint behavior."""
import io
import unittest
from email.message import Message
from unittest.mock import patch
from urllib.error import HTTPError

from scripts.http_smoke import check


class Response(io.BytesIO):
    def __init__(self, body, content_type):
        super().__init__(body)
        self.status = 200
        self.headers = Message()
        self.headers['Content-Type'] = content_type


class SmokeTests(unittest.TestCase):
    def responses(self, unknown):
        return [Response(b'{"status":"ok","environment":"verification"}', 'application/json'),
                Response(b'DevOps Laboratory Work 1 38419', 'text/html'), unknown]

    def test_accepts_correct_endpoints(self):
        error = HTTPError('http://localhost/unknown', 404, 'Not found', {}, None)
        with patch('scripts.http_smoke.build_opener') as factory, \
                patch.dict('os.environ', {'APP_ENV': 'verification', 'STUDENT_ID': '38419'}):
            factory.return_value.open.side_effect = self.responses(error)
            check()
            self.assertEqual(factory.return_value.open.call_count, 3)

    def test_rejects_unknown_route_returning_success(self):
        with patch('scripts.http_smoke.build_opener') as factory, \
                patch.dict('os.environ', {'APP_ENV': 'verification', 'STUDENT_ID': '38419'}):
            factory.return_value.open.side_effect = self.responses(Response(b'wrong', 'text/plain'))
            with self.assertRaisesRegex(AssertionError, 'Unknown route'):
                check()

    def test_rejects_wrong_environment(self):
        with patch('scripts.http_smoke.build_opener') as factory, \
                patch.dict('os.environ', {'APP_ENV': 'production'}):
            factory.return_value.open.side_effect = self.responses(None)
            with self.assertRaises(AssertionError):
                check()
