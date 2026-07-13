import os
import sys
import json
import pytest
import queue
import unittest
from unittest.mock import MagicMock, patch
# --- Add src directory to sys.path so chatbot modules can be imported ---
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
from chatbot import stt_handler
class TestSttHandlerVulnerabilities(unittest.TestCase):
    # -------------------------------------------------------------------------
    # 1. Unbounded Queue Growth Verification (High Severity)
    # -------------------------------------------------------------------------
    @patch("chatbot.stt_handler.queue.Queue")
    @patch("chatbot.stt_handler.KaldiRecognizer")
    @patch("chatbot.stt_handler._get_model")
    @patch("chatbot.stt_handler.sd.RawInputStream")
    def test_unbounded_queue_growth(self, mock_stream, mock_get_model, mock_rec_cls, mock_queue_class):
        """
        Verify that queue.Queue is initialized with a maximum size constraint (bounded).
        """
        mock_rec = MagicMock()
        mock_rec_cls.return_value = mock_rec
        mock_rec.AcceptWaveform.return_value = True
        mock_rec.Result.return_value = '{"text": "hello"}'
        # Trigger STT
        stt_handler.listen_to_mic()
        # Check queue initialization params
        mock_queue_class.assert_called_once()
        args, kwargs = mock_queue_class.call_args
        maxsize = kwargs.get("maxsize", 0)
        self.assertEqual(maxsize, 1000, "Queue is not bounded to a size of 1000.")
    # -------------------------------------------------------------------------
    # 2. Missing Microphone Exception Handling Verification (High Severity)
    # -------------------------------------------------------------------------
    @patch("chatbot.stt_handler.KaldiRecognizer")
    @patch("chatbot.stt_handler._get_model")
    @patch("chatbot.stt_handler.sd.RawInputStream")
    def test_missing_microphone_exception_handling(self, mock_stream, mock_get_model, mock_rec_cls):
        """
        Verify that sd.RawInputStream exceptions (no mic, denied permission)
        are caught gracefully and return an empty string.
        """
        mock_rec = MagicMock()
        mock_rec_cls.return_value = mock_rec
        
        # Simulate sounddevice stream failure (e.g. no microphone connected)
        mock_stream.side_effect = RuntimeError("Host error: Default input device not found")
        # Expect the routine to catch the error and return empty string
        result = stt_handler.listen_to_mic()
        self.assertEqual(result, "")
    # -------------------------------------------------------------------------
    # 3. Unsafe JSON Parsing Assumption Verification (High Severity)
    # -------------------------------------------------------------------------
    @patch("chatbot.stt_handler.queue.Queue")
    @patch("chatbot.stt_handler.KaldiRecognizer")
    @patch("chatbot.stt_handler._get_model")
    @patch("chatbot.stt_handler.sd.RawInputStream")
    def test_unsafe_json_parsing_assumption(self, mock_stream, mock_get_model, mock_rec_cls, mock_queue_cls):
        """
        Verify that if Vosk output is malformed, it is handled gracefully and returns "".
        """
        mock_rec = MagicMock()
        mock_rec_cls.return_value = mock_rec
        mock_rec.AcceptWaveform.return_value = True
        
        # Mock Vosk returning invalid JSON
        mock_rec.Result.return_value = "{invalid_json_data"
        
        mock_queue = MagicMock()
        # Feed one fake chunk of audio data then stop
        mock_queue.get.side_effect = [b"audio_chunk", queue.Empty]
        mock_queue_cls.return_value = mock_queue
        # Expect it to handle it gracefully and return ""
        result = stt_handler.listen_to_mic()
        self.assertEqual(result, "")
    # -------------------------------------------------------------------------
    # 4. No Audio Device Validation Verification (Medium Severity)
    # -------------------------------------------------------------------------
    def test_no_audio_device_validation(self):
        """
        Verify that `sd.query_devices` is never called before opening raw stream
        to check if input devices exist on the system.
        """
        import inspect
        source = inspect.getsource(stt_handler.listen_to_mic)
        self.assertNotIn("query_devices", source)
    # -------------------------------------------------------------------------
    # 5. No Audio Device Selection Support Verification (Medium Severity)
    # -------------------------------------------------------------------------
    def test_no_audio_device_selection_support(self):
        """
        Verify that listen_to_mic doesn't accept a device selection index or parameter.
        """
        import inspect
        sig = inspect.signature(stt_handler.listen_to_mic)
        self.assertNotIn("device", sig.parameters)
        self.assertNotIn("device_index", sig.parameters)
    # -------------------------------------------------------------------------
    # 6. Hardcoded English Speech Model Verification (Medium Severity)
    # -------------------------------------------------------------------------
    def test_hardcoded_english_speech_model(self):
        """
        Verify that the default directory points to a hardcoded English Vosk model folder.
        """
        self.assertTrue(hasattr(stt_handler, "DEFAULT_VOSK_DIR"))
        self.assertIn("vosk-model-small-en-us-0.15", stt_handler.DEFAULT_VOSK_DIR)
    # -------------------------------------------------------------------------
    # 7. Silent Failure Modes Verification (Medium Severity)
    # -------------------------------------------------------------------------
    @patch("chatbot.stt_handler.KaldiRecognizer")
    @patch("chatbot.stt_handler._get_model")
    @patch("chatbot.stt_handler.sd.RawInputStream")
    def test_silent_failure_modes(self, mock_stream, mock_get_model, mock_rec_cls):
        """
        Verify that different failure cases (like timeout/silence or cancellation)
        silently return an empty string "" instead of error status or codes.
        """
        mock_rec = MagicMock()
        mock_rec_cls.return_value = mock_rec
        
        # Test case: Silence timeout (simulate by letting listen_to_mic run with max_silence_sec=0)
        result = stt_handler.listen_to_mic(max_silence_sec=0)
        self.assertEqual(result, "")
        # Test case: should_stop cancellation trigger
        result = stt_handler.listen_to_mic(should_stop=lambda: True)
        self.assertEqual(result, "")
    # -------------------------------------------------------------------------
    # 8. Global Model Initialization Race Condition Verification (Low Severity)
    # -------------------------------------------------------------------------
    def test_global_model_initialization_race_condition(self):
        """
        Verify that `_get_model` accesses and creates the global `_MODEL`
        without using any mutex locks or synchronized guards.
        """
        import inspect
        source = inspect.getsource(stt_handler._get_model)
        self.assertNotIn("Lock", source)
        self.assertNotIn("acquire", source)
    # -------------------------------------------------------------------------
    # 9. No Confidence Threshold Validation Verification (Low Severity)
    # -------------------------------------------------------------------------
    @patch("chatbot.stt_handler.queue.Queue")
    @patch("chatbot.stt_handler.KaldiRecognizer")
    @patch("chatbot.stt_handler._get_model")
    @patch("chatbot.stt_handler.sd.RawInputStream")
    def test_no_confidence_threshold_validation(self, mock_stream, mock_get_model, mock_rec_cls, mock_queue_cls):
        """
        Verify that the text returned is directly trusted from JSON result without
        checking Vosk confidence metrics or rejecting background noise.
        """
        mock_rec = MagicMock()
        mock_rec_cls.return_value = mock_rec
        mock_rec.AcceptWaveform.return_value = True
        
        # Vosk results can include details like 'conf' or confidence.
        # But our code simply does: json.loads(rec.Result()).get("text", "").strip()
        mock_rec.Result.return_value = '{"text": "noise", "confidence": 0.05}'
        
        mock_queue = MagicMock()
        mock_queue.get.side_effect = [b"chunk", queue.Empty]
        mock_queue_cls.return_value = mock_queue
        result = stt_handler.listen_to_mic()
        
        # Verify the chatbot accepted the transcription despite extremely low confidence
        self.assertEqual(result, "noise")
if __name__ == "__main__":
    unittest.main()