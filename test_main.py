import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Mock telethon before importing main
mock_telethon = MagicMock()
sys.modules['telethon'] = mock_telethon
sys.modules['telethon.sessions'] = MagicMock()
sys.modules['telethon.tl.types'] = MagicMock()

# Now import main
# We need to set env vars so main doesn't crash on os.getenv check
os.environ["API_ID"] = "12345"
os.environ["API_HASH"] = "hash123"
os.environ["SESSION"] = "session_string"

import main
from main import apply_styles, styles

class TestBotLogic(unittest.TestCase):
    def setUp(self):
        # Reset styles before each test
        styles["bold"] = False
        styles["italic"] = False

    def test_apply_styles_none(self):
        self.assertEqual(apply_styles("hello"), "hello")

    def test_apply_styles_bold(self):
        styles["bold"] = True
        self.assertEqual(apply_styles("hello"), "**hello**")

    def test_apply_styles_italic(self):
        styles["italic"] = True
        self.assertEqual(apply_styles("hello"), "__hello__")

    def test_apply_styles_both(self):
        styles["bold"] = True
        styles["italic"] = True
        self.assertEqual(apply_styles("hello"), "__**hello**__")

    def test_initialization_values(self):
        self.assertEqual(main.API_ID, 12345)
        self.assertEqual(main.API_HASH, "hash123")
        self.assertEqual(main.SESSION, "session_string")

if __name__ == "__main__":
    unittest.main()
