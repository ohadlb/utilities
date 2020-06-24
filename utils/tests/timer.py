from io import StringIO
from time import sleep
from typeguard.importhook import install_import_hook
import unittest
from unittest.mock import patch

with install_import_hook('utils.timer'):
    from ..timer import ExecutionTimer

DELAY = 0.5


class Callback:
    def __call__(self, interval):
        self.interval = interval


class TimerTest(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_none(self, mock_stdout):
        with ExecutionTimer(output=None) as e:
            sleep(DELAY)
        self.assertGreater(e.interval, DELAY)
        self.assertEqual(mock_stdout.getvalue(), '')

    @patch('sys.stdout', new_callable=StringIO)
    def test_string(self, mock_stdout):
        with ExecutionTimer() as e:
            sleep(DELAY)
        self.assertGreater(e.interval, DELAY)
        self.assertTrue(mock_stdout.getvalue().startswith('Execution completed in'))
        self.assertIn(f'{e.interval:0.2f}', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_callback(self, mock_stdout):
        cb = Callback()
        with ExecutionTimer(output=cb) as e:
            sleep(DELAY)
        self.assertGreater(e.interval, DELAY)
        self.assertEqual(e.interval, cb.interval)
        self.assertEqual(mock_stdout.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
