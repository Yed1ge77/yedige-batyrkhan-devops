"""Unit and isolated local HTTP tests; no existing server is required."""
import io
import json
import tempfile
import unittest
from email.parser import BytesParser
from pathlib import Path
from unittest.mock import patch

from app.main import configured_handler
from app.student import load_student


class StudentTests(unittest.TestCase):
    def test_configuration_loads(self):
        self.assertEqual(len(load_student()), 5)

    def test_name(self):
        self.assertEqual(load_student()["full_name"], "Batyrkhan Yedige Yerlanuly")

    def test_student_id(self):
        self.assertEqual(load_student()["student_id"], "38419")

    def test_group_university_course(self):
        student = load_student()
        self.assertEqual(student["group"], "IT2-2302")
        self.assertEqual(student["university"], "IITU")
        self.assertEqual(student["course"], "DevOps")

    def test_invalid_configuration(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1] / "logs") as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_student(path)

    def test_missing_configuration(self):
        with self.assertRaises(FileNotFoundError):
            load_student(Path(__file__).parent / "nonexistent-student.json")


class MemoryConnection:
    """Socket substitute: the real handler reads and writes HTTP bytes in memory."""
    def __init__(self, request):
        self.request = io.BytesIO(request)
        self.response = io.BytesIO()

    def makefile(self, mode, buffering=-1):
        return self.request

    def sendall(self, data):
        self.response.write(data)


class HTTPTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict("os.environ", {}, clear=True)
        environment.start()
        self.addCleanup(environment.stop)

    def get(self, path):
        connection = MemoryConnection(
            f"GET {path} HTTP/1.0\r\nHost: localhost\r\n\r\n".encode("ascii")
        )
        configured_handler()(connection, ("127.0.0.1", 12345), None)
        headers, body = connection.response.getvalue().split(b"\r\n\r\n", 1)
        status_line, header_lines = headers.split(b"\r\n", 1)
        status = int(status_line.split()[1])
        parsed_headers = BytesParser().parsebytes(header_lines + b"\r\n\r\n")
        self.assertEqual(int(parsed_headers["Content-Length"]), len(body))
        return status, parsed_headers, body

    def test_home_status_and_content_type(self):
        status, headers, _ = self.get("/")
        self.assertEqual(status, 200)
        self.assertEqual(headers.get_content_type(), "text/html")

    def test_home_student_information(self):
        _, _, body = self.get("/")
        for value in load_student().values():
            self.assertIn(value, body.decode("utf-8"))

    def test_health_status_and_json(self):
        status, headers, body = self.get("/health")
        self.assertEqual(status, 200)
        self.assertEqual(headers.get_content_type(), "application/json")
        self.assertEqual(json.loads(body), {"status": "ok", "environment": "development"})

    def test_default_environment_on_page(self):
        self.assertIn(b"Environment: development", self.get("/")[2])

    def test_custom_environment(self):
        with patch.dict("os.environ", {"APP_ENV": "testing"}):
            self.assertEqual(json.loads(self.get("/health")[2])["environment"], "testing")
            self.assertIn(b"Environment: testing", self.get("/")[2])

    def test_student_environment_overrides(self):
        settings = {"STUDENT_NAME": "Test", "STUDENT_SURNAME": "Student",
                    "STUDENT_GROUP": "TEST-1", "STUDENT_ID": "999"}
        with patch.dict("os.environ", settings):
            body = self.get("/")[2].decode()
        for value in ("Test Student", "TEST-1", "999"):
            self.assertIn(value, body)
        self.assertEqual(load_student()["student_id"], "38419")

    def test_unknown_route(self):
        status, headers, body = self.get("/unknown")
        self.assertEqual(status, 404)
        self.assertEqual(headers.get_content_type(), "text/plain")
        self.assertEqual(body, b"Not found\n")

    def test_environment_html_is_escaped(self):
        with patch.dict("os.environ", {"APP_ENV": "<script>alert(1)</script>"}):
            body = self.get("/")[2]
        self.assertIn(b"&lt;script&gt;", body)
        self.assertNotIn(b"<script>", body)


if __name__ == "__main__":
    unittest.main()
