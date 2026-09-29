from __future__ import annotations

import numpy as np
import pytest

from claude_router import ClaudeRouter


@pytest.fixture
def router() -> ClaudeRouter:
    return ClaudeRouter()


def test_route_returns_expected_shape(monkeypatch: pytest.MonkeyPatch, router: ClaudeRouter) -> None:
    research = router.centroids["research"]
    monkeypatch.setattr(router, "_embed", lambda _: research)

    result = router.route("Evaluate this paper")

    assert result["category"] == "research"
    assert result["model"].startswith("claude-")
    assert result["scaffold_key"] == "insight-first"
    assert result["low_confidence"] is False


def test_low_confidence_falls_back_to_opus(monkeypatch: pytest.MonkeyPatch, router: ClaudeRouter) -> None:
    zeros = np.zeros_like(next(iter(router.centroids.values())))
    monkeypatch.setattr(router, "_embed", lambda _: zeros)

    result = router.route("Ambiguous prompt")

    assert result["tier"] == "opus"
    assert result["scaffold_key"] is None
    assert result["low_confidence"] is True


def test_build_prompt_includes_scaffold(monkeypatch: pytest.MonkeyPatch, router: ClaudeRouter) -> None:
    evaluation = router.centroids["eval"]
    monkeypatch.setattr(router, "_embed", lambda _: evaluation)

    result = router.route("Score this summary")
    prompt = router.build_prompt("Score this summary", result)

    assert prompt.endswith("Score this summary")
    assert result["scaffold_text"] in prompt


def test_empty_input_fails_fast(router: ClaudeRouter) -> None:
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        router.route("   ")


def test_cli_version_flag_does_not_route_it_as_a_query(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    from claude_router import __version__
    from claude_router import router as router_module

    monkeypatch.setattr(router_module.sys, "argv", ["claude-router", "--version"])
    monkeypatch.setattr(
        router_module,
        "ClaudeRouter",
        lambda *a, **k: pytest.fail("--version must not build the router or call the embedder"),
    )

    router_module._cli()

    assert capsys.readouterr().out.strip() == f"claude-router {__version__}"
