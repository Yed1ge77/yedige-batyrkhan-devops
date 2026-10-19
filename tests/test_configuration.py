"""Regression checks for invalid configuration and server startup settings."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.main import main
from app.student import FIELDS, load_student


class ConfigurationTests(unittest.TestCase):
    def test_rejects_invalid_field_types_and_empty_values(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parents[1] / 'logs') as directory:
            path = Path(directory) / 'student.json'
            for field in FIELDS:
                for invalid in (None, '', '   ', 38419, []):
                    with self.subTest(field=field, value=invalid):
                        student = load_student()
                        student[field] = invalid
                        path.write_text(json.dumps(student), encoding='utf-8')
                        with self.assertRaises(ValueError):
                            load_student(path)

    def test_rejects_non_object_and_malformed_json(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parents[1] / 'logs') as directory:
            path = Path(directory) / 'student.json'
            for content in ('[]', 'null', '{broken'):
                with self.subTest(content=content):
                    path.write_text(content, encoding='utf-8')
                    with self.assertRaises(ValueError):
                        load_student(path)

    def test_invalid_port_exits_without_creating_server(self):
        for port in ('0', '-1', '65536', 'abc'):
            with self.subTest(port=port), patch.dict('os.environ', {'PORT': port}), \
                    patch('app.main.create_server') as factory, \
                    contextlib.redirect_stderr(io.StringIO()) as errors:
                self.assertEqual(main(), 1)
                factory.assert_not_called()
                self.assertIn('Cannot start application', errors.getvalue())

    def test_configurable_host_and_port(self):
        with patch.dict('os.environ', {'HOST': '127.0.0.1', 'PORT': '8123'}), \
                patch('app.main.create_server') as factory, \
                contextlib.redirect_stdout(io.StringIO()):
            factory.return_value.__enter__.return_value.serve_forever.side_effect = KeyboardInterrupt
            self.assertEqual(main(), 0)
            factory.assert_called_once_with('127.0.0.1', 8123)

    def test_bind_failure_is_reported(self):
        with patch('app.main.create_server', side_effect=OSError('Address already in use')), \
                contextlib.redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(main(), 1)
            self.assertIn('Address already in use', errors.getvalue())
