from pathlib import Path

version = Path("VERSION").read_text(encoding="utf-8-sig").strip()
assert version in {"0.5.71", "0.5.72", "0.5.74"}

manifest = Path("extension/manifest.json").read_text(encoding="utf-8-sig")
assert f"AI Bridge Local {version}" in manifest

background = Path("extension/background.js").read_text(encoding="utf-8-sig")
assert "aiBridgeDiscoverDirectTargetTab" in background
assert "activeMatches" in background
assert "activeMatches[0] || matches[0]" in background
assert "registry[targetChatId]" in background

print("OK smoke_refresh_direct_target_0571")
