import os
import unittest
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path to import bot.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bot

class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = bot.bot

    def test_get_log_channel_no_env(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(bot.get_log_channel())

    def test_get_log_channel_with_env(self):
        mock_channel = MagicMock()
        with patch.dict(os.environ, {"LOG_CHANNEL_ID": "12345"}):
            with patch.object(bot.bot, 'get_channel', return_value=mock_channel):
                result = bot.get_log_channel()
                self.assertEqual(result, mock_channel)
                bot.bot.get_channel.assert_called_once_with(12345)

    def test_on_member_join(self):
        mock_member = MagicMock()
        mock_member.__str__ = lambda: "TestUser"
        mock_channel = MagicMock()
        
        with patch.dict(os.environ, {"LOG_CHANNEL_ID": "12345"}):
            with patch.object(bot.bot, 'get_channel', return_value=mock_channel):
                import asyncio
                asyncio.run(bot.on_member_join(mock_member))
                mock_channel.send.assert_called_once()
                call_args = mock_channel.send.call_args[0][0]
                self.assertIn("joined the server", call_args)

    def test_on_member_remove(self):
        mock_member = MagicMock()
        mock_member.__str__ = lambda: "TestUser"
        mock_channel = MagicMock()
        
        with patch.dict(os.environ, {"LOG_CHANNEL_ID": "12345"}):
            with patch.object(bot.bot, 'get_channel', return_value=mock_channel):
                import asyncio
                asyncio.run(bot.on_member_remove(mock_member))
                mock_channel.send.assert_called_once()
                call_args = mock_channel.send.call_args[0][0]
                self.assertIn("left the server", call_args)

    def test_on_member_update_name_change(self):
        mock_before = MagicMock()
        mock_before.name = "OldName"
        mock_before.__str__ = lambda: "OldName"
        
        mock_after = MagicMock()
        mock_after.name = "NewName"
        mock_after.__str__ = lambda: "NewName"
        
        mock_channel = MagicMock()
        
        with patch.dict(os.environ, {"LOG_CHANNEL_ID": "12345"}):
            with patch.object(bot.bot, 'get_channel', return_value=mock_channel):
                import asyncio
                asyncio.run(bot.on_member_update(mock_before, mock_after))
                mock_channel.send.assert_called_once()
                call_args = mock_channel.send.call_args[0][0]
                self.assertIn("changed their name", call_args)

    def test_on_member_update_no_name_change(self):
        mock_before = MagicMock()
        mock_before.name = "SameName"
        
        mock_after = MagicMock()
        mock_after.name = "SameName"
        
        mock_channel = MagicMock()
        
        with patch.dict(os.environ, {"LOG_CHANNEL_ID": "12345"}):
            with patch.object(bot.bot, 'get_channel', return_value=mock_channel):
                import asyncio
                asyncio.run(bot.on_member_update(mock_before, mock_after))
                mock_channel.send.assert_not_called()

if __name__ == "__main__":
    unittest.main()
