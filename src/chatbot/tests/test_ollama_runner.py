 
import os
import sys
import json
import inspect
import pytest
from unittest.mock import MagicMock
 
# --- make the `chatbot` package importable ----------------------------------
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
 
from chatbot import ollama_runner
 
 
# ==============================================================================
# Safety net + helpers
# ==============================================================================
 
@pytest.fixture(autouse=True)
def _default_offline_client(monkeypatch):
    """
    Replaces the real Ollama client with a blank MagicMock by default, so no
    test can ever accidentally hit a real local Ollama server. Tests that
    need specific chat/list/embeddings behavior configure their own mock
    and monkeypatch.setattr it themselves (overriding this default).
    """
    monkeypatch.setattr(ollama_runner, "ollama_client", MagicMock())
    yield
 
 
def mock_chat_returning(monkeypatch, content):
    """Convenience: makes ollama_client.chat(...) return a given message content."""
    client = MagicMock()
    client.chat.return_value = {"message": {"content": content}}
    monkeypatch.setattr(ollama_runner, "ollama_client", client)
    return client
 
 
# ==============================================================================
# Smoke test
# ==============================================================================
 
class TestSmoke:
    def test_run_ollama_happy_path(self, monkeypatch):
        mock_chat_returning(monkeypatch, "  a clean response  ")
        result = ollama_runner.run_ollama("hello")
        assert result == "a clean response"
 
    def test_run_ollama_vision_happy_path(self, monkeypatch):
        content = (
            "Some reasoning text.\n```json\n"
            '{"vision_summary": "ok", "component_counts": {}, '
            '"circuit_analysis": {"circuit_type": "x", "design_errors": [], "design_warnings": []}, '
            '"components": [], "values": {}}'
            "\n```"
        )
        mock_chat_returning(monkeypatch, content)
        result = ollama_runner.run_ollama_vision("prompt", b"fakebytes")
        parsed = json.loads(result)
        assert parsed["vision_summary"] == "ok"
 
 
# ==============================================================================
# OLM-01 — Missing model validation
# ==============================================================================
 
class TestMissingModelValidation:
    """run_ollama()/run_ollama_vision() never check the configured model
    against ollama_client.list() before using it. A missing/renamed model
    only surfaces as a generic chat failure deep inside the try/except,
    not as an early, specific, user-actionable error."""
 
    def test_run_ollama_never_calls_list_before_chat(self, monkeypatch):
        client = MagicMock()
        client.list.return_value = {"models": [{"name": "some-other-model"}]}
        client.chat.side_effect = Exception("model 'qwen2.5:3b' not found, try pulling it first")
        monkeypatch.setattr(ollama_runner, "ollama_client", client)
 
        result = ollama_runner.run_ollama("hello")
 
        client.list.assert_not_called()
        assert "[Error]" in result, (
            "Pre-fix: a missing model only shows up as a generic chat "
            "exception with no pre-flight validation. Post-fix: assert "
            "client.list() IS called and a specific 'model not installed' "
            "message is returned instead."
        )
 
    def test_run_ollama_vision_never_calls_list_before_chat(self, monkeypatch):
        client = MagicMock()
        client.list.return_value = {"models": [{"name": "some-other-model"}]}
        client.chat.side_effect = Exception("model 'minicpm-v:latest' not found")
        monkeypatch.setattr(ollama_runner, "ollama_client", client)
 
        result = ollama_runner.run_ollama_vision("prompt", b"fakebytes")
 
        client.list.assert_not_called()
        data = json.loads(result)
        assert data["circuit_analysis"]["circuit_type"] == "Error"
 
 
# ==============================================================================
# OLM-02 — get_embedding() returns None on failure
# ==============================================================================
 
class TestEmbeddingReturnsNone:
    def test_embedding_failure_returns_none_not_raise(self, monkeypatch):
        client = MagicMock()
        client.embeddings.side_effect = Exception("connection refused")
        monkeypatch.setattr(ollama_runner, "ollama_client", client)
 
        result = ollama_runner.get_embedding("some text")
 
        assert result is None, (
            "Pre-fix: failures are swallowed into a bare None with no "
            "distinction from 'embedding was legitimately empty'. Post-fix "
            "(retry / structured exception): update this to assert a retry "
            "happened (client.embeddings.call_count > 1) or that a specific "
            "exception type is raised instead of returning None."
        )
 
 
# ==============================================================================
# OLM-03 — Invalid settings-file model names accepted unchecked
# ==============================================================================
 
class TestInvalidSettingsModels:
    """settings.json can contain any string as a model name; nothing
    cross-checks it against the models Ollama actually has installed."""
 
    def test_arbitrary_model_name_loaded_without_cross_check(self, tmp_path, monkeypatch):
        bogus_settings = tmp_path / "settings.json"
        bogus_settings.write_text(json.dumps({
            "text_model": "totally-made-up-model-xyz",
            "vision_model": "another-fake-model",
        }))
        monkeypatch.setattr(ollama_runner, "_SETTINGS_PATH", str(bogus_settings))
 
        loaded = ollama_runner.load_model_settings()
        assert loaded["text_model"] == "totally-made-up-model-xyz"
 
    def test_reload_pulls_unchecked_model_into_active_config(self, tmp_path, monkeypatch):
        bogus_settings = tmp_path / "settings.json"
        bogus_settings.write_text(json.dumps({
            "text_model": "totally-made-up-model-xyz",
            "vision_model": "another-fake-model",
        }))
        monkeypatch.setattr(ollama_runner, "_SETTINGS_PATH", str(bogus_settings))
 
        client = MagicMock()
        client.list.return_value = {"models": [{"name": "qwen2.5:3b"}]}
        monkeypatch.setattr(ollama_runner, "ollama_client", client)
 
        ollama_runner.reload_model_settings()
 
        assert ollama_runner.TEXT_MODELS["default"] == "totally-made-up-model-xyz"
        client.list.assert_not_called()
        # Post-fix: reload_model_settings() should call list_available_models()
        # (or similar) and reject/flag names that aren't actually installed.
 
 
# ==============================================================================
# OLM-04 — Documentation / code model-name mismatch
# ==============================================================================
 
class TestDocCodeMismatch:
    def test_current_default_model_constants(self):
        """Documents the CURRENT code-side truth so any future change to
        these constants is caught here too (keep in sync with the doc check
        below)."""
        assert ollama_runner._DEFAULT_TEXT_MODEL == "qwen2.5:3b"
        assert ollama_runner._DEFAULT_VISION_MODEL == "minicpm-v:latest"
 
    def test_documentation_does_not_reference_stale_model_names(self):
        """
        Searches for README_CHATBOT.md / CHATBOT_ENHANCEMENT_PROPOSAL.md
        near this test file and checks they don't still reference the old
        model names (qwen2.5-coder:3b, qwen2.5-vl:3b) that the code no
        longer uses. Skips gracefully if the docs aren't found at any of
        the guessed locations — adjust `search_roots` to your repo layout
        if that happens.
        """
        chatbot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        search_roots = [
            chatbot_dir,
            os.path.join(chatbot_dir, ".."),
            os.path.join(chatbot_dir, "..", ".."),
        ]
        doc_names = ("README_CHATBOT.md", "CHATBOT_ENHANCEMENT_PROPOSAL.md")
        stale_names = ("qwen2.5-coder:3b", "qwen2.5-vl:3b")
 
        found_any = False
        for root in search_roots:
            for name in doc_names:
                path = os.path.join(root, name)
                if os.path.isfile(path):
                    found_any = True
                    with open(path, encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    for stale in stale_names:
                        assert stale not in content, (
                            f"{path} still references stale model name "
                            f"'{stale}', but code now uses "
                            f"{ollama_runner._DEFAULT_TEXT_MODEL} / "
                            f"{ollama_runner._DEFAULT_VISION_MODEL}."
                        )
 
        if not found_any:
            pytest.skip(
                "README_CHATBOT.md / CHATBOT_ENHANCEMENT_PROPOSAL.md not "
                "found near this test file — update search_roots to point "
                "at their real location to make this check meaningful."
            )
 
 
# ==============================================================================
# OLM-05 — No retry logic on transient failures
# ==============================================================================
 
class TestNoRetryLogic:
    def test_text_transient_failure_is_not_retried(self, monkeypatch):
        client = MagicMock()
        client.chat.side_effect = Exception("connection reset by peer")
        monkeypatch.setattr(ollama_runner, "ollama_client", client)
 
        ollama_runner.run_ollama("hello")
 
        assert client.chat.call_count == 1, (
            "Pre-fix: a single transient failure ends the request "
            "immediately. Post-fix (exponential backoff retry): assert "
            "call_count equals the configured max-retry count."
        )
 
    def test_vision_transient_failure_is_not_retried(self, monkeypatch):
        client = MagicMock()
        client.chat.side_effect = Exception("timeout")
        monkeypatch.setattr(ollama_runner, "ollama_client", client)
 
        ollama_runner.run_ollama_vision("prompt", b"fakebytes")
 
        assert client.chat.call_count == 1
 
 
# ==============================================================================
# OLM-06 — Fragile JSON extraction from vision output
# ==============================================================================
 
class TestFragileJsonExtraction:
    def test_no_braces_in_output_falls_back_to_empty_object_string(self, monkeypatch):
        mock_chat_returning(monkeypatch, "I'm not able to analyze this image right now.")
        result = ollama_runner.run_ollama_vision("prompt", b"fakebytes")
        assert result == "{}"
 
    def test_two_separate_json_blocks_produce_invalid_json(self, monkeypatch):
        """
        find('{') grabs the FIRST opening brace and rfind('}') grabs the
        LAST closing brace, with no validation in between. If the model
        rambles and includes an example JSON snippet before its real
        answer, the slice spans both objects plus the prose between them
        — producing a string that isn't valid JSON at all.
        """
        content = (
            'Here is an example format: {"foo": "bar"} '
            'Now here is my real answer: '
            '{"vision_summary": "ok", "component_counts": {}, '
            '"circuit_analysis": {"circuit_type": "x", "design_errors": [], "design_warnings": []}, '
            '"components": [], "values": {}}'
        )
        mock_chat_returning(monkeypatch, content)
        result = ollama_runner.run_ollama_vision("prompt", b"fakebytes")
 
        with pytest.raises(json.JSONDecodeError):
            json.loads(result)
 
 
# ==============================================================================
# OLM-07 — Non-streaming responses
# ==============================================================================
 
class TestNonStreamingResponses:
    def test_text_chat_does_not_request_streaming(self, monkeypatch):
        client = mock_chat_returning(monkeypatch, "ok")
        ollama_runner.run_ollama("hello")
        _, kwargs = client.chat.call_args
        assert kwargs.get("stream") in (None, False)
 
    def test_vision_chat_does_not_request_streaming(self, monkeypatch):
        client = mock_chat_returning(monkeypatch, "{}")
        ollama_runner.run_ollama_vision("prompt", b"fakebytes")
        _, kwargs = client.chat.call_args
        assert kwargs.get("stream") in (None, False)
 
 
# ==============================================================================
# OLM-08 — Hardcoded context window
# ==============================================================================
 
class TestHardcodedContextWindow:
    def test_num_ctx_values_are_literal_constants_in_source(self):
        source = inspect.getsource(ollama_runner)
        assert '"num_ctx": 2048' in source
        assert '"num_ctx": 8192' in source
        assert "os.environ" not in source, (
            "Pre-fix: num_ctx values are hardcoded literals, not read from "
            "config/env. Post-fix: move them into config and update this "
            "test to confirm it's read dynamically instead."
        )
 
 
# ==============================================================================
# OLM-09 — Weak image-input validation (length-only check)
# ==============================================================================
 
class TestWeakImageInputValidation:
    def test_long_non_base64_string_is_forwarded_without_validation(self, monkeypatch):
        client = mock_chat_returning(monkeypatch, "{}")
 
        # Clearly NOT valid base64 (spaces, punctuation), but length > 100
        fake_image_string = "this is definitely not base64 data!! " * 5
        assert len(fake_image_string) > 100
 
        ollama_runner.run_ollama_vision("prompt", fake_image_string)
 
        _, kwargs = client.chat.call_args
        sent_images = kwargs["messages"][1]["images"]
        assert sent_images == [fake_image_string], (
            "Pre-fix: any string over 100 characters is assumed to be "
            "valid base64 and forwarded as-is to Ollama, with zero actual "
            "decoding/validation. Post-fix: add explicit base64 validation "
            "and assert a ValueError/rejection happens instead."
        )
 
    def test_short_string_raises_invalid_format_internally(self, monkeypatch):
        mock_chat_returning(monkeypatch, "{}")
        result = ollama_runner.run_ollama_vision("prompt", "short_string")
        data = json.loads(result)
        assert "failed" in data["vision_summary"].lower()
 
 
# ==============================================================================
# OLM-10 — Information disclosure through raw error messages
# ==============================================================================
 
class TestErrorMessageDisclosure:
    def test_run_ollama_leaks_raw_exception_text(self, monkeypatch):
        sensitive_message = "Connection failed to internal-host-10.0.5.23:11434 (token abc123 invalid)"
        client = MagicMock()
        client.chat.side_effect = Exception(sensitive_message)
        monkeypatch.setattr(ollama_runner, "ollama_client", client)
 
        result = ollama_runner.run_ollama("hello")
 
        assert sensitive_message in result, (
            "Pre-fix: raw exception text reaches the caller/UI verbatim. "
            "Post-fix: sanitize the user-facing message and log full "
            "details separately, then assert the sensitive text is NOT "
            "in the returned string."
        )
 
    def test_run_ollama_vision_leaks_raw_exception_text(self, monkeypatch):
        sensitive_message = "FileNotFoundError: /home/user/.ssh/private_schematics/config"
        client = MagicMock()
        client.chat.side_effect = Exception(sensitive_message)
        monkeypatch.setattr(ollama_runner, "ollama_client", client)
 
        result = ollama_runner.run_ollama_vision("prompt", b"fakebytes")
        data = json.loads(result)
 
        assert sensitive_message[:50] in data["vision_summary"]
 
 
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
 