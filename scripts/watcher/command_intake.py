import argparse
import json
import os
import subprocess
import time

CATALOG = {
 'inspect_repo': {'risk': 'read_only', 'steps': [['git', 'status', '-sb'], ['git', 'log', '--oneline', '--decorate', '-5']]},
 'inspect_docs': {'risk': 'read_only', 'steps': [['git', 'status', '-sb'], ['python', 'scripts/watcher/smoke_docs.py']]},
 'run_smokes': {'risk': 'validation', 'steps': [['python', 'scripts/watcher/smoke_version_alignment.py'], ['python', 'scripts/watcher/smoke_command_builder_validate.py'], ['python', 'scripts/watcher/smoke_docs.py']]},
}

RISK_POLICY = {
 'read_only': 'execute directly',
 'validation': 'execute with timeout',
}

def build_plan(intent, cwd, command_id):
 if intent not in CATALOG:
  raise SystemExit('unknown intent: ' + intent)
 abs_cwd = os.path.abspath(cwd)
 if not os.path.isdir(abs_cwd):
  raise SystemExit('cwd does not exist: ' + cwd)
 item = CATALOG[intent]
 steps = []
 for index, command in enumerate(item['steps'], 1):
  steps.append({'index': index, 'type': 'run', 'command': command})
 return {
  'schema': 'ai_bridge_local.command_intake_plan',
  'schema_version': 1,
  'command_id': command_id,
  'intent': intent,
  'cwd': abs_cwd,
  'risk': item['risk'],
  'risk_policy': RISK_POLICY[item['risk']],
  'status': 'planned',
  'steps': steps,
 }

def execute_plan(plan, timeout):
 results = []
 status = 'acked'
 for step in plan['steps']:
  cp = subprocess.run(step['command'], cwd=plan['cwd'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
  results.append({'index': step['index'], 'command': step['command'], 'return_code': cp.returncode, 'stdout_tail': cp.stdout[-2000:], 'stderr_tail': cp.stderr[-2000:]})
  if cp.returncode != 0:
   status = 'failed'
   break
 out = dict(plan)
 out['status'] = status
 out['results'] = results
 return out

def main():
 parser = argparse.ArgumentParser()
 parser.add_argument('--intent', required=True, choices=sorted(CATALOG))
 parser.add_argument('--cwd', default='.')
 parser.add_argument('--command-id', default='intake_' + str(int(time.time())))
 parser.add_argument('--execute', action='store_true')
 parser.add_argument('--timeout', type=int, default=120)
 args = parser.parse_args()
 plan = build_plan(args.intent, args.cwd, args.command_id)
 if args.execute:
  plan = execute_plan(plan, args.timeout)
 print(json.dumps(plan, indent=2, sort_keys=True))
 return 0 if plan['status'] in {'planned', 'acked'} else 1

if __name__ == '__main__':
 raise SystemExit(main())
