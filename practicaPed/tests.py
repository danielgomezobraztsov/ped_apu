import unittest
import subprocess
import time
import os
import signal
import re

TEST_SOCKET = "/tmp/test_server.sock"

class TestUnixSocketServerClient(unittest.TestCase):

    def setUp(self):
        # Start the server before each test
        self.server_proc = subprocess.Popen(
            ["python3", "serv.py", TEST_SOCKET],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(0.2)  # Give the server time to start

    def tearDown(self):
        # Stop the server after each test
        self.server_proc.send_signal(signal.SIGTERM)
        try:
            self.server_proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            self.server_proc.kill()
        if os.path.exists(TEST_SOCKET):
            os.unlink(TEST_SOCKET)

    def test_time_command(self):
        output = subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, "TIME"], timeout=2
        ).decode().strip()
        self.assertRegex(output, r"\d{2}:\d{2}:\d{2}")

    def test_date_command(self):
        output = subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, "DATE"], timeout=2
        ).decode().strip()
        self.assertRegex(output, r"\d{4}-\d{2}-\d{2}")

    def test_invalid_command(self):
        output = subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, "FOO"], timeout=2
        ).decode().strip()
        self.assertEqual(output, "ERROR")

    def test_empty_command(self):
        output = subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, ""], timeout=2
        ).decode().strip()
        self.assertEqual(output, "ERROR")

    def test_long_command(self):
        long_str = "A" * 1024
        output = subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, long_str], timeout=2
        ).decode().strip()
        self.assertEqual(output, "ERROR")

    def test_lowercase_time(self):
        output = subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, "time"], timeout=2
        ).decode().strip()
        self.assertEqual(output, "ERROR")

    def test_lowercase_date(self):
        output = subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, "date"], timeout=2
        ).decode().strip()
        self.assertEqual(output, "ERROR")

    def test_sequential_time(self):
        output1 = subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, "TIME"], timeout=2
        ).decode().strip()
        self.assertRegex(output1, r"\d{2}:\d{2}:\d{2}")

    def test_sequential_date(self):
        subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, "TIME"], timeout=2
        )
        output2 = subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, "DATE"], timeout=2
        ).decode().strip()
        self.assertRegex(output2, r"\d{4}-\d{2}-\d{2}")

    def test_sequential_invalid(self):
        subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, "TIME"], timeout=2
        )
        subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, "DATE"], timeout=2
        )
        output3 = subprocess.check_output(
            ["python3", "cli.py", TEST_SOCKET, "INVALID"], timeout=2
        ).decode().strip()
        self.assertEqual(output3, "ERROR")

    def test_server_socket_cleanup(self):
        # This test checks cleanup after server is stopped
        self.tearDown()  # Stop server and cleanup
        self.assertFalse(os.path.exists(TEST_SOCKET))
        # Start server again for future tests
        self.setUp()

    def test_nonexistent_server_socket(self):
        bogus_socket = "/tmp/nonexistent_socket.sock"
        if os.path.exists(bogus_socket):
            os.unlink(bogus_socket)
        try:
            with self.assertRaises(subprocess.CalledProcessError):
                subprocess.check_output(
                    ["python3", "cli.py", bogus_socket, "TIME"],
                    timeout=2, stderr=subprocess.STDOUT
                )
        finally:
            if os.path.exists(bogus_socket):
                os.unlink(bogus_socket)

if __name__ == "__main__":
    unittest.main()
