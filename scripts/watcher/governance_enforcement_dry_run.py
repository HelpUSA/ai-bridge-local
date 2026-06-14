import argparse
import json


DESTRUCTIVE_TERMS = [
    "remove-item",
    " rmdir",
    " del ",
    "format ",
    "drop table",
    "git reset --hard",
    "git clean -fd",
    "shutil.rmtree",
]

MUTATING_TERMS = [
    "git commit",
    "git push",
    "set-content",
    "add-content",
    "writealltext",
    "move-item",
    "copy-item",
    "new-item",
    "mkdir",
]

READ_ONLY_TERMS = [
    "git status",
    "git log",
    "git diff",
    "get-content",
    "select-string",
    "node --check",
    "smoke_",
]


def classify(command_text):
    text = " " + command_text.lower().strip() + " "
    if not text.strip():
        return "empty"
    for term in DESTRUCTIVE_TERMS:
        if term in text:
            return "destructive"
    for term in MUTATING_TERMS:
        if term in text:
            return "mutating"
    for term in READ_ONLY_TERMS:
        if term in text:
            return "read_only_or_dry_run"
    return "unknown_review_required"


def simulate(command):
    command_text = " ".join(command)
    risk = classify(command_text)
    would_block = risk == "destructive"
    requires_review = risk in ("destructive", "unknown_review_required")
    return {
        "command": command,
        "command_text": command_text,
        "dry_run": True,
        "enforcement_enabled": False,
        "risk_level": risk,
        "would_block_if_enforced": would_block,
        "requires_manual_review": requires_review,
        "blocks_execution_now": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--command", nargs=argparse.REMAINDER, default=[])
    args = parser.parse_args()
    result = simulate(args.command)
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print("AI_BRIDGE_LOCAL_ENFORCEMENT_DRY_RUN")
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
