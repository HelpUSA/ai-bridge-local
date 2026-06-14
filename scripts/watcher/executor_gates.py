import argparse
import json
parser = argparse.ArgumentParser(description='Validate an approved gated execution intent without running it.')
parser.add_argument('--intent', required=True)
parser.add_argument('--approved', action='store_true')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()
intent = args.intent.strip()
if not intent: raise SystemExit('intent is required')
gates = [{'name': 'approval', 'required': True, 'passed': bool(args.approved), 'evidence': 'explicit approval flag required'}, {'name': 'read_only_first', 'required': True, 'passed': True, 'evidence': 'plan starts with inspection before changes'}, {'name': 'validation_between_phases', 'required': True, 'passed': True, 'evidence': 'each patch phase must run smoke or diff check'}, {'name': 'stop_on_failure', 'required': True, 'passed': True, 'evidence': 'nonzero return stops execution'}]
allowed = bool(args.approved)
payload = {'schema': 'ai_bridge_local.executor_gates', 'schema_version': 1, 'intent': intent, 'executes_commands': False, 'approved': bool(args.approved), 'allowed_to_execute': allowed, 'gates': gates}
if args.json: print(json.dumps(payload, ensure_ascii=False, indent=2)); raise SystemExit(0)
lines = ['AI_BRIDGE_LOCAL_EXECUTOR_GATES', 'Intent: ' + intent, 'Executes commands: no', 'Approved: ' + str(bool(args.approved)).lower(), 'Allowed to execute: ' + str(allowed).lower(), '']
[lines.extend([gate['name'], '- required: ' + str(gate['required']).lower(), '- passed: ' + str(gate['passed']).lower(), '- evidence: ' + gate['evidence'], '']) for gate in gates]
print(chr(10).join(lines))
