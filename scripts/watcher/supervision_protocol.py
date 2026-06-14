
import argparse
import json

parser = argparse.ArgumentParser(description="Formal supervision protocol for AI Bridge Local chats")
parser.add_argument("--phase", default="all", choices=["all", "plan", "readonly", "patch", "release", "handoff"])
parser.add_argument("--json", action="store_true")
args = parser.parse_args()

PHASES = [
    {
        "phase": "plan",
        "owner": "executor",
        "fiscal_gate": "plan_review",
        "required_evidence": ["objective", "scope", "risk", "read_only_first", "validation_plan"],
        "rule": "executor must propose plan before changing files",
    },
    {
        "phase": "readonly",
        "owner": "executor",
        "fiscal_gate": "readonly_review",
        "required_evidence": ["git_status", "git_log", "relevant_files", "roadmap_refs"],
        "rule": "executor must inspect current state before patching",
    },
    {
        "phase": "patch",
        "owner": "executor",
        "fiscal_gate": "patch_review",
        "required_evidence": ["diff_stat", "diff_check", "targeted_smokes", "no_unexpected_files"],
        "rule": "patch must be narrow and validated before commit",
    },
    {
        "phase": "release",
        "owner": "release_manager",
        "fiscal_gate": "release_audit",
        "required_evidence": ["version_alignment", "release_check", "tag", "push", "status_clean"],
        "rule": "release must include final audit and reference commit",
    },
    {
        "phase": "handoff",
        "owner": "supervisor",
        "fiscal_gate": "handoff_acceptance",
        "required_evidence": ["current_head", "changed_files", "validations", "pending_items", "next_safe_command"],
        "rule": "handoff must be enough for another chat to continue safely",
    },
]

ROLES = {
    "supervisor": "selects next roadmap item, checks scope, records state",
    "executor": "runs read-only inspection and applies approved patches",
    "fiscal": "reviews plan, diff, validations and release evidence",
    "documenter": "keeps guide, roadmap and version notes aligned",
}

GATES = [
    "no_patch_before_readonly",
    "no_commit_before_smokes",
    "no_tag_before_release_check",
    "no_handoff_without_next_safe_command",
]

phases = PHASES if args.phase == "all" else [phase for phase in PHASES if phase["phase"] == args.phase]
payload = {
    "ok": True,
    "schema": "ai_bridge_local.supervision_protocol",
    "schema_version": 1,
    "filters": {"phase": args.phase},
    "roles": ROLES,
    "gates": GATES,
    "phases": phases,
}

if args.json:
    print(json.dumps(payload, indent=2, sort_keys=True))
else:
    print("AI_BRIDGE_LOCAL_SUPERVISION_PROTOCOL")
    print("roles")
    for role, description in ROLES.items():
        print(role + ": " + description)
    print("gates")
    for gate in GATES:
        print("- " + gate)
    print("phases")
    for phase in phases:
        print("phase " + phase["phase"])
        print("owner " + phase["owner"])
        print("fiscal_gate " + phase["fiscal_gate"])
        print("required_evidence " + ", ".join(phase["required_evidence"]))
        print("rule " + phase["rule"])
